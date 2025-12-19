"""
Agent service for the RAG Chatbot backend.

This module provides the main orchestration service using OpenAI Agents SDK
to combine embedding generation, vector search, and OpenAI API calls to provide
RAG-based responses with source citations.
"""
import os
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner
from agents.extensions.memory import SQLAlchemySession

from ..models.database import ChatSession, ChatMessage
from ..models.schemas import ChatRequest, ChatResponse, SourceCitation
from ..utils.validators import sanitize_input, validate_message_content
from .embedding_service import embedding_service
from .vector_service import vector_service


# Load environment variables (override=True forces .env to override system env vars)
load_dotenv(override=True)
# Strip any whitespace/carriage returns from API key
openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
if openai_api_key:
    print(f"API Key loaded.....")
else:
    print("API Key Not Found!!")
# Initialize OpenAI async client
client = AsyncOpenAI(api_key=openai_api_key)


class AgentService:
    """
    Service class for handling the main chatbot orchestration logic using OpenAI Agents SDK.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize the agent service.

        Args:
            model: OpenAI model to use for responses
        """
        self.model = model
        # Initialize the main RAG agent
        self.agent = Agent(
            name="RAG Chatbot",
            instructions="""
            You are an AI assistant for the Physical AI & Humanoid Robotics course.
            Your purpose is to answer questions about the course content based on the provided context.

            Guidelines:
            1. Only use information from the provided context to answer questions
            2. If the context doesn't contain information to answer the question, say so
            3. Be accurate and cite sources when possible
            4. Keep responses concise but informative
            5. If the question is off-topic (not related to Physical AI, Humanoid Robotics, ROS 2, NVIDIA Isaac, etc.), politely decline and ask about course topics
            """,
            model=self.model
        )

    def get_or_create_session(self, db: Session, user_id: str, session_id: Optional[str] = None) -> ChatSession:
        """
        Get an existing session or create a new one.

        Args:
            db: Database session
            user_id: User identifier
            session_id: Session identifier (if None, creates new)

        Returns:
            ChatSession object
        """
        if session_id:
            # Try to get existing session
            session = db.query(ChatSession).filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id
            ).first()

            if session:
                # Update the last accessed time
                session.updated_at = datetime.utcnow()
                db.commit()
                return session
            else:
                # Session ID provided but doesn't exist, create with that ID
                session = ChatSession(
                    id=session_id,
                    user_id=user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(session)
                try:
                    db.commit()
                    db.refresh(session)
                    return session
                except Exception as e:
                    db.rollback()
                    # If there's a duplicate key error, it means another request created it
                    # Try to fetch it again
                    session = db.query(ChatSession).filter(
                        ChatSession.id == session_id,
                        ChatSession.user_id == user_id
                    ).first()
                    if session:
                        return session
                    else:
                        raise e
        else:
            # Create new session with generated ID
            new_session_id = str(uuid.uuid4())
            session = ChatSession(
                id=new_session_id,
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session

    async def query(self, db: Session, chat_request: ChatRequest) -> ChatResponse:
        """
        Process a chat query and return a response with source citations.

        Args:
            db: Database session
            chat_request: Chat request with user message and context

        Returns:
            ChatResponse with AI response and source citations
        """
        # Validate and sanitize input
        is_valid, error_msg = validate_message_content(chat_request.message)
        if not is_valid:
            raise ValueError(error_msg)

        sanitized_message = sanitize_input(chat_request.message)

        # Get or create session
        session = self.get_or_create_session(db, chat_request.user_id, chat_request.session_id)

        # If selected text is provided, include it in the context
        context_text = sanitized_message
        if chat_request.selected_text:
            context_text = f"Context from selected text: {chat_request.selected_text}\n\nQuestion: {sanitized_message}"

        # Generate embedding for the query
        query_embedding = await embedding_service.generate_embedding(context_text)

        # Search for similar content in the vector database
        search_results = await vector_service.search_similar(query_embedding, limit=5)

        # Build context from search results
        context_parts = []
        sources = []
        for result in search_results:
            context_parts.append(result["text"])

            # Create source citation
            source = SourceCitation(
                page=result["page"],
                section=result["section"],
                url=result["url"],
                relevance_score=result["relevance_score"]
            )
            sources.append(source.dict())

        # Combine all context parts
        combined_context = "\n\n".join(context_parts)

        # Create the full prompt for the AI with the retrieved context
        full_prompt = f"""
        Course Context:
        {combined_context}

        User Question: {sanitized_message}

        Please provide an accurate answer based on the course context, and cite your sources.
        """

        # Get the database URL and convert it to asyncpg format for the Agent SDK
        db_url = os.getenv("NEON_DATABASE_URL", "").strip()

        # Convert to asyncpg URL format if it's not already in the async format
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

        # For Neon connections, we might need to remove SSL parameters that asyncpg doesn't support
        # Remove sslmode and other parameters that asyncpg doesn't recognize
        if "?sslmode=" in db_url:
            # Split the URL to remove problematic parameters
            base_url = db_url.split('?')[0]
            # Add back only the parameters that asyncpg supports
            db_url = base_url

        # Create SQLAlchemy session for conversation history
        # This will maintain context across multiple interactions
        sql_session = SQLAlchemySession.from_url(
            session.id,
            url=db_url,
            create_tables=True
        )

        # Run the agent with the full prompt and session
        result = await Runner.run(
            self.agent,
            full_prompt,
            session=sql_session
        )

        # Extract the response from the agent
        response_text = result.final_output

        # Create chat message in database
        user_message = ChatMessage(
            session_id=session.id,
            role="user",
            content=sanitized_message,
            selected_text=chat_request.selected_text,
            sources=sources,  # Store sources in message (already dict format)
            metadata_={}  # Empty metadata for now
        )
        db.add(user_message)

        # Create AI response message
        ai_message = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=response_text,
            sources=sources,  # Store sources in AI message too (already dict format)
            metadata_={}  # Empty metadata for now
        )
        db.add(ai_message)
        db.commit()

        # Return the response with sources and session info
        return ChatResponse(
            response=response_text,
            sources=sources,
            session_id=session.id,
            timestamp=datetime.utcnow()
        )

    async def get_conversation_history(self, db: Session, session_id: str, limit: int = 10, offset: int = 0) -> List[ChatMessage]:
        """
        Retrieve conversation history for a session.

        Args:
            db: Database session
            session_id: Session identifier
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of ChatMessage objects
        """
        messages = db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.timestamp.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()

        # Reverse to get chronological order (oldest first)
        return list(reversed(messages))

    async def process_feedback(self, db: Session, session_id: str, message_id: str, feedback: str) -> bool:
        """
        Process user feedback on a response.

        Args:
            db: Database session
            session_id: Session identifier
            message_id: Message identifier
            feedback: User feedback

        Returns:
            True if successful, False otherwise
        """
        # In a full implementation, this would store feedback for analysis
        # For now, we'll just return True
        return True

    async def reset_session(self, db: Session, session_id: str) -> bool:
        """
        Reset a session by clearing its conversation history.

        Args:
            db: Database session
            session_id: Session identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete all messages in the session
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()

            # Update the session's updated_at timestamp
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session:
                session.updated_at = datetime.utcnow()
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error resetting session: {e}")
            return False


# Global instance for use in other modules
agent_service = AgentService()