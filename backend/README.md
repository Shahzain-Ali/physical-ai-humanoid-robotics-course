# RAG Chatbot Backend

Backend API for the RAG Chatbot Integration feature, providing semantic search and AI-powered Q&A capabilities for the Physical AI & Humanoid Robotics course content.

## Overview

This FastAPI application serves as the backend for the chatbot, handling:
- Semantic search over course content using Qdrant vector database
- AI-powered question answering using OpenAI API
- Chat history persistence using Neon Postgres
- Content embedding and management

## Architecture

- **Framework**: FastAPI for high-performance async API
- **Database**: Neon Serverless Postgres for chat history
- **Vector Store**: Qdrant Cloud for semantic search
- **AI Provider**: OpenAI for embeddings and chat completions

## Prerequisites

Before running the backend, ensure you have:

1. **Python 3.10+** installed
2. **API Keys** configured:
   - OpenAI API key
   - Qdrant Cloud URL and API key
   - Neon Postgres connection string

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys and connection strings.

### 4. Initialize Vector Database

Set up Qdrant collection:

```bash
python scripts/setup_qdrant.py
```

### 5. Embed Course Content

Process and embed all course content:

```bash
python scripts/embed_content.py
```

## Running the Server

Start the backend server:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `POST /chat` - Process user queries and return AI responses with citations
- `GET /history` - Retrieve chat history for a session
- `GET /health` - Health check endpoint

For detailed API specifications, see `specs/002-rag-chatbot/contracts/`.

## Scripts

- `scripts/setup_qdrant.py` - Initialize Qdrant collection
- `scripts/embed_content.py` - Process and embed course content
- `scripts/check_collection.py` - Verify collection status

## Development

For development, run with auto-reload:

```bash
uvicorn src.main:app --reload
```

## Deployment

This backend is designed for deployment to Railway. See `backend/railway.toml` for deployment configuration.

For more details, see the [Quickstart Guide](../specs/002-rag-chatbot/quickstart.md).