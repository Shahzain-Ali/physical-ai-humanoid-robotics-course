"""
Database configuration for the RAG Chatbot backend.

This module sets up the SQLAlchemy engine and session configuration
for connecting to Neon Serverless Postgres with appropriate settings
for serverless environments.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Load environment variables from .env file
load_dotenv()

# Load database URL from environment variables
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "").strip()

# Configure the database engine with NullPool for serverless compatibility
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Serverless-friendly - no connection pooling
    echo=False,  # Set to True for SQL query logging during development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to get database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()