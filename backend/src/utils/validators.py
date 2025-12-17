"""
Input validation utilities for the RAG Chatbot backend.

This module provides functions to sanitize and validate user input
to prevent injection attacks and ensure data quality.
"""
import re
from typing import Optional
import html


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and other injection attacks.

    Args:
        text: User input text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return text

    # Remove potentially dangerous characters/sequences
    # HTML encode special characters
    sanitized = html.escape(text)

    # Remove any script tags (case insensitive)
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)

    # Remove javascript: and data: URIs
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'data:', '', sanitized, flags=re.IGNORECASE)

    # Remove eval and other dangerous functions
    sanitized = re.sub(r'eval\s*\(', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'exec\s*\(', '', sanitized, flags=re.IGNORECASE)

    return sanitized.strip()


def validate_query_length(query: str, max_length: int = 2000) -> bool:
    """
    Validate that a query doesn't exceed maximum length.

    Args:
        query: Query string to validate
        max_length: Maximum allowed length (default: 2000)

    Returns:
        True if valid, False otherwise
    """
    if not query:
        return False

    return len(query) <= max_length


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.

    Args:
        user_id: User ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not user_id:
        return False

    # Allow alphanumeric, hyphens, and underscores, 1-255 characters
    pattern = r'^[a-zA-Z0-9_-]{1,255}$'
    return bool(re.match(pattern, user_id))


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format (UUID-like string).

    Args:
        session_id: Session ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not session_id:
        return False

    # Allow UUID format (with or without hyphens) or alphanumeric, 1-36 characters
    pattern = r'^[a-zA-Z0-9_-]{1,36}$'
    return bool(re.match(pattern, session_id))


def validate_selected_text(selected_text: Optional[str]) -> bool:
    """
    Validate selected text length.

    Args:
        selected_text: Selected text to validate

    Returns:
        True if valid, False otherwise
    """
    if selected_text is None:
        return True  # None is valid (no text selected)

    if not selected_text:
        return True  # Empty string is valid (no text selected)

    # Maximum length for selected text (same as query limit)
    return len(selected_text) <= 2000


def validate_message_content(message: str) -> tuple[bool, Optional[str]]:
    """
    Validate message content completely.

    Args:
        message: Message content to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Message cannot be empty"

    if len(message) > 2000:
        return False, "Message exceeds maximum length of 2000 characters"

    # Check for excessive repetition (potential spam)
    # Count consecutive identical characters
    if re.search(r'(.)\1{9,}', message):  # More than 10 consecutive identical characters
        return False, "Message contains excessive repetition"

    return True, None


def clean_message_content(message: str) -> str:
    """
    Clean and normalize message content.

    Args:
        message: Message content to clean

    Returns:
        Cleaned message content
    """
    if not message:
        return message

    # Sanitize the input
    cleaned = sanitize_input(message)

    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()

    return cleaned