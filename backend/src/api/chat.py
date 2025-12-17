"""
Chat API router for the RAG Chatbot backend.

This module defines the FastAPI router for chat-related endpoints
including the main /chat endpoint that processes user queries and
returns AI-generated responses with source citations.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from ..models.schemas import ChatRequest, ChatResponse
from ..services.agent_service import agent_service
from ..config import get_db
from ..utils.validators import validate_message_content, sanitize_input


# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process a chat query and return a response with source citations.

    Args:
        chat_request: Chat request with user message and context
        db: Database session dependency

    Returns:
        ChatResponse with AI response and source citations
    """
    try:
        # Validate the request
        is_valid, error_msg = validate_message_content(chat_request.message)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Log the incoming request
        logger.info(f"Processing chat request for user: {chat_request.user_id}, session: {chat_request.session_id}")

        # Process the query using the agent service
        response = await agent_service.query(db, chat_request)

        # Log successful response
        logger.info(f"Successfully processed chat request for session: {response.session_id}")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)

        # Raise a generic error to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while processing your request"
        )


@router.post("/chat/stream", response_model=ChatResponse)
async def chat_stream_endpoint(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process a chat query and return a streaming response.

    Args:
        chat_request: Chat request with user message and context
        db: Database session dependency

    Returns:
        Streaming response with AI response and source citations
    """
    try:
        # Validate the request
        is_valid, error_msg = validate_message_content(chat_request.message)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Log the incoming request
        logger.info(f"Processing streaming chat request for user: {chat_request.user_id}, session: {chat_request.session_id}")

        # Process the query using the agent service
        response = await agent_service.query(db, chat_request)

        # Log successful response
        logger.info(f"Successfully processed streaming chat request for session: {response.session_id}")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error processing streaming chat request: {str(e)}", exc_info=True)

        # Raise a generic error to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while processing your request"
        )


@router.post("/session")
async def create_session_endpoint():
    """
    Create a new chat session for ChatKit.
    This endpoint returns a session identifier that ChatKit can use.
    """
    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    # In a real implementation, you would create the session in your database
    # For now, we'll just return the session ID

    return {
        "session_id": session_id,
        "status": "created",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health")
async def chat_health():
    """
    Health check endpoint for the chat service.
    """
    return {
        "status": "ok",
        "service": "chat",
        "timestamp": datetime.utcnow().isoformat()
    }