"""
Pydantic schemas for the RAG Chatbot backend.

This module defines the request and response models using Pydantic
for data validation and serialization.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    """Enumeration for message roles."""
    user = "user"
    assistant = "assistant"


class SourceCitation(BaseModel):
    """Schema for source citations in chat responses."""
    page: str = Field(..., description="Source page name (e.g., '03-ros2.md')")
    section: str = Field(..., description="Section name within the page")
    url: str = Field(..., description="URL to the specific section")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score of the citation")


class ChatRequest(BaseModel):
    """Schema for chat request payload."""
    user_id: str = Field(..., min_length=1, max_length=255, description="Unique identifier for the user")
    message: str = Field(..., min_length=1, max_length=2000, description="User's message to the chatbot")
    session_id: Optional[str] = Field(default=None, min_length=1, max_length=36, description="Session identifier (will be created if not provided)")
    selected_text: Optional[str] = Field(default=None, max_length=2000, description="Text selected by user on the page (if any)")


class ChatResponse(BaseModel):
    """Schema for chat response payload."""
    response: str = Field(..., description="AI-generated response to the user's message")
    sources: List[SourceCitation] = Field(default_factory=list, description="List of source citations used in the response")
    session_id: str = Field(..., description="Session identifier (newly created or existing)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the response")


class HistoryRequest(BaseModel):
    """Schema for history request query parameters."""
    session_id: str = Field(..., min_length=1, max_length=36, description="Session identifier to retrieve history for")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum number of messages to return")
    offset: int = Field(default=0, ge=0, description="Number of messages to skip (for pagination)")


class ChatMessageSchema(BaseModel):
    """Schema for individual chat messages in history response."""
    id: str
    role: Role
    content: str
    timestamp: datetime
    sources: Optional[List[SourceCitation]] = None
    selected_text: Optional[str] = None


class HistoryResponse(BaseModel):
    """Schema for history response payload."""
    messages: List[ChatMessageSchema] = Field(..., description="List of messages in the chat history")
    total_count: int = Field(..., description="Total number of messages available in the session")
    session_id: str = Field(..., description="Session identifier")