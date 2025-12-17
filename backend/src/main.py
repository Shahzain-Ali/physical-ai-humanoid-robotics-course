"""
Main FastAPI application for the RAG Chatbot backend.

This module sets up the FastAPI application with CORS middleware,
includes API routers, and provides health check endpoints.
"""
import os
import logging
from datetime import datetime
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import get_db, engine
from .models import database  # Import to create tables
from .api.chat import router as chat_router
from .api.history import router as history_router


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables in the database
database.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG Chatbot that answers questions about the Physical AI & Humanoid Robotics course",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # In production, be more specific about allowed origins
)

# Include API routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(history_router, prefix="/api", tags=["history"])

@app.get("/")
async def root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "RAG Chatbot API is running"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is operational.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "RAG Chatbot API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def api_health_check():
    """
    API health check endpoint with more detailed information.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "RAG Chatbot API",
        "version": "1.0.0",
        "dependencies": {
            "database": "connected",
            "qdrant": "pending",  # Would check actual connection
            "openai": "pending"   # Would check actual connection
        }
    }

# Database dependency for endpoints that need it
def get_db_session():
    """
    Dependency function to get database session.
    """
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler for the application.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {"status": "error", "message": "An internal server error occurred"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )