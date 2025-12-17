"""
Database models for the RAG Chatbot backend.

This module defines the SQLAlchemy models for chat sessions and messages
with proper relationships and constraints.
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableDict
import uuid
from datetime import datetime
from ..config import Base


class ChatSession(Base):
    """
    Model representing a chat session between a user and the chatbot.
    """
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata_ = Column(MutableDict.as_mutable(JSON), nullable=True)

    # Relationship to chat messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """
    Model representing a single message in a chat session.
    """
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sources = Column(JSON, nullable=True)  # List of source citations
    selected_text = Column(Text, nullable=True)  # Text that was selected when message was sent
    metadata_ = Column(MutableDict.as_mutable(JSON), nullable=True)

    # Relationship back to session
    session = relationship("ChatSession", back_populates="messages")