"""
History API router for the RAG Chatbot backend.

This module defines the FastAPI router for chat history-related endpoints
including retrieving conversation history for a session.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from ..models.schemas import HistoryRequest, HistoryResponse, ChatMessageSchema
from ..services.agent_service import agent_service
from ..models.database import ChatMessage, ChatSession
from ..config import get_db
from ..utils.validators import validate_session_id


# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
async def get_history_endpoint(
    session_id: str = Query(..., min_length=1, max_length=36, description="Session identifier to retrieve history for"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of messages to return"),
    offset: int = Query(0, ge=0, description="Number of messages to skip (for pagination)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve chat history for a specific session.

    Args:
        session_id: Session identifier to retrieve history for
        limit: Maximum number of messages to return (default: 50, max: 100)
        offset: Number of messages to skip (for pagination)
        db: Database session dependency

    Returns:
        HistoryResponse with chat messages and metadata
    """
    try:
        # Validate session ID format
        if not validate_session_id(session_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid session ID format"
            )

        # Log the incoming request
        logger.info(f"Retrieving chat history for session: {session_id}, limit: {limit}, offset: {offset}")

        # Verify the session exists and belongs to the user
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Get conversation history from the agent service
        messages = await agent_service.get_conversation_history(db, session_id, limit, offset)

        # Convert to response schema
        chat_messages = []
        for msg in messages:
            chat_message = ChatMessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp,
                sources=msg.sources,
                selected_text=msg.selected_text
            )
            chat_messages.append(chat_message)

        # Get total count for pagination
        total_count = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).count()

        # Create response
        response = HistoryResponse(
            messages=chat_messages,
            total_count=total_count,
            session_id=session_id
        )

        # Log successful response
        logger.info(f"Successfully retrieved {len(chat_messages)} messages for session: {session_id}")

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving chat history for session {session_id}: {str(e)}", exc_info=True)

        # Raise a generic error to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while retrieving chat history"
        )


@router.delete("/history/{session_id}")
async def delete_history_endpoint(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete chat history for a specific session.

    Args:
        session_id: Session identifier to delete history for
        db: Database session dependency

    Returns:
        Success message
    """
    try:
        # Validate session ID format
        if not validate_session_id(session_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid session ID format"
            )

        # Log the incoming request
        logger.info(f"Deleting chat history for session: {session_id}")

        # Verify the session exists
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Delete all messages in the session
        deleted_count = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()

        # Update session's updated_at timestamp
        session.updated_at = datetime.utcnow()
        db.commit()

        # Log successful deletion
        logger.info(f"Successfully deleted {deleted_count} messages for session: {session_id}")

        return {
            "status": "success",
            "message": f"Successfully deleted {deleted_count} messages",
            "session_id": session_id
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Error deleting chat history for session {session_id}: {str(e)}", exc_info=True)

        # Raise a generic error to the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred while deleting chat history"
        )


@router.get("/history/health")
async def history_health():
    """
    Health check endpoint for the history service.
    """
    return {
        "status": "ok",
        "service": "history",
        "timestamp": datetime.utcnow().isoformat()
    }