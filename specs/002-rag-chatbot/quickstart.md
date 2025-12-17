# RAG Chatbot - Developer Quickstart

**Feature**: 002-rag-chatbot
**Target Audience**: Developers setting up the chatbot locally for development and testing
**Estimated Setup Time**: 10-15 minutes

## Prerequisites

Before starting, ensure you have:

- **Python 3.10+** installed (`python --version`)
- **Node.js 18+** installed (`node --version`)
- **Git** installed
- **API Keys** configured in `.env` file:
  - `OPENAI_API_KEY` (OpenAI account)
  - `QDRANT_URL` and `QDRANT_API_KEY` (Qdrant Cloud free tier)
  - `NEON_DATABASE_URL` (Neon Serverless Postgres free tier)

## Quick Start (3 Commands)

If you're in a hurry, run these three commands from the project root:

```bash
# 1. Setup backend and initialize databases
cd backend && python -m venv venv && source venv/bin/activate && \
pip install -r requirements.txt && \
python scripts/setup_qdrant.py && \
python scripts/embed_content.py

# 2. Start backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &

# 3. Start frontend (from project root in new terminal)
cd .. && npm install @openai/chatkit-js && npm start
```

Then open http://localhost:3000 and click the chat button!

---

## Detailed Setup Instructions

### Part 1: Backend Setup (5-7 minutes)

#### Step 1.1: Create Python Virtual Environment

```bash
cd backend
python -m venv venv
```

**Activate the virtual environment**:
- **Linux/Mac**: `source venv/bin/activate`
- **Windows CMD**: `venv\Scripts\activate.bat`
- **Windows PowerShell**: `venv\Scripts\Activate.ps1`

You should see `(venv)` in your terminal prompt.

#### Step 1.2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages** (partial list):
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `openai` - OpenAI API client with Agent SDK
- `qdrant-client` - Vector database client
- `sqlalchemy[asyncio]` - Database ORM
- `pydantic` - Data validation
- `python-dotenv` - Environment variable loader

**Installation time**: ~2-3 minutes

#### Step 1.3: Configure Environment Variables

The `.env` file should already exist in the project root. If not, create it:

```bash
# From backend directory
cp ../.env .env
```

**Verify required variables are set**:
```bash
cat .env | grep -E "OPENAI_API_KEY|QDRANT|NEON"
```

You should see output like:
```
OPENAI_API_KEY=sk-proj-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
NEON_DATABASE_URL=postgresql://...
```

#### Step 1.4: Initialize Qdrant Collection

```bash
python scripts/setup_qdrant.py
```

**Expected output**:
```
Connecting to Qdrant at https://your-cluster.qdrant.io...
✓ Connected successfully
Creating collection 'book_content'...
✓ Collection created with config:
  - Vector size: 1536
  - Distance metric: Cosine
  - HNSW parameters: m=16, ef_construct=100
✓ Setup complete!
```

**What this does**:
- Creates Qdrant collection named `book_content`
- Configures for OpenAI `text-embedding-3-small` (1536 dimensions)
- Sets up HNSW indexing for fast semantic search

**Troubleshooting**:
- **Error: Collection already exists**: Delete it in Qdrant dashboard or run with `--force-recreate` flag
- **Error: Invalid API key**: Check `QDRANT_API_KEY` in `.env`
- **Error: Connection timeout**: Verify `QDRANT_URL` is correct

#### Step 1.5: Embed Course Content

```bash
python scripts/embed_content.py
```

**Expected output**:
```
Loading course content from docs/...
✓ Found 47 Markdown files

Chunking content...
✓ Generated 4,832 chunks (avg 742 tokens per chunk)

Generating embeddings... (this takes 2-3 minutes)
[===========================================] 4832/4832 chunks
✓ Generated 4,832 embeddings (cost: ~$0.10)

Uploading to Qdrant...
[===========================================] 4832/4832 chunks
✓ Uploaded successfully

Summary:
  Pages processed: 47
  Chunks created: 4,832
  Total tokens: ~3.6M
  Qdrant storage: ~28MB
  Estimated cost: $0.096
```

**What this does**:
- Reads all `.md` files from `docs/` directory
- Chunks content (500-1000 tokens with 100 token overlap)
- Generates embeddings using OpenAI API
- Stores chunks with metadata in Qdrant collection

**Troubleshooting**:
- **Error: OPENAI_API_KEY not found**: Check `.env` file
- **Error: Rate limit exceeded**: Wait 60 seconds and retry (OpenAI free tier limits)
- **Error: Collection not found**: Run `setup_qdrant.py` first (Step 1.4)

#### Step 1.6: Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Will watch for changes in these directories: ['/backend/src']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**What this does**:
- Starts FastAPI application
- Enables auto-reload on code changes (`--reload`)
- Exposes API on port 8000
- Connects to Qdrant and Neon Postgres

**Keep this terminal open**. The server must run continuously.

#### Step 1.7: Test Backend (New Terminal)

Open a new terminal and test the `/chat` endpoint:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "What are ROS 2 nodes?",
    "session_id": "test_session_001"
  }'
```

**Expected response** (formatted):
```json
{
  "response": "ROS 2 nodes are independent processes that perform computation. Each node typically represents a single, modular purpose - for example, controlling the robot's wheels, publishing sensor data, or performing localization. Nodes communicate with each other by publishing messages to named topics and subscribing to topics of interest.",
  "sources": [
    {
      "page": "03-ros2.md",
      "section": "Understanding Nodes",
      "url": "/docs/03-ros2#understanding-nodes",
      "relevance_score": 0.89
    },
    {
      "page": "03-ros2.md",
      "section": "Node Communication",
      "url": "/docs/03-ros2#node-communication",
      "relevance_score": 0.82
    }
  ],
  "session_id": "test_session_001"
}
```

**Success indicators**:
- ✓ Response includes AI-generated answer
- ✓ Sources array contains course page citations
- ✓ Session ID matches request
- ✓ Response time < 3 seconds

**Test health check**:
```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "ok",
  "timestamp": "2025-12-17T10:30:00.123Z"
}
```

---

### Part 2: Frontend Setup (3-5 minutes)

#### Step 2.1: Install ChatKit SDK

**From project root** (not backend directory):

```bash
npm install @openai/chatkit-js
```

**Expected output**:
```
added 15 packages, and audited 2341 packages in 8s
```

#### Step 2.2: Configure API Endpoint

Edit `docusaurus.config.js` and add `customFields`:

```javascript
// docusaurus.config.js
module.exports = {
  // ... existing config ...

  customFields: {
    // Backend API URL (defaults to localhost for development)
    apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000'
  },

  // ... rest of config ...
};
```

**Alternative**: Set environment variable before running `npm start`:
```bash
export REACT_APP_API_URL=http://localhost:8000
npm start
```

#### Step 2.3: Start Docusaurus Development Server

```bash
npm start
```

**Expected output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at http://localhost:3000/

✔ Client
  Compiled successfully in 8.23s

webpack compiled successfully
```

**Browser should auto-open** to http://localhost:3000

#### Step 2.4: Test Chat Widget

**Manual test steps**:

1. **Verify widget visible**:
   - Look for floating chat button in bottom-right corner
   - Button should have chat bubble icon

2. **Open chat panel**:
   - Click the chat button
   - Panel should slide in from right side
   - Should show empty conversation with input box

3. **Send test message**:
   - Type: "What is NVIDIA Isaac?"
   - Press Enter or click Send button
   - Should see typing indicator immediately

4. **Verify response**:
   - AI response appears within 3 seconds
   - Response includes information about NVIDIA Isaac
   - Source citations shown below response (e.g., "Source: 05-isaac.md")
   - Citations are clickable and navigate to course page

5. **Test text selection** (if implemented):
   - Highlight any paragraph on a course page
   - "Ask about this" tooltip should appear
   - Click tooltip → chat opens with selection as context

**Success indicators**:
- ✓ Chat widget loads on all course pages
- ✓ Messages send and receive successfully
- ✓ Source citations are clickable
- ✓ Chat history persists when navigating between pages

---

## Running Tests

### Backend Unit Tests

```bash
cd backend
pytest tests/unit/ -v
```

**Expected output**:
```
tests/unit/test_chunker.py::test_chunk_by_headers PASSED
tests/unit/test_chunker.py::test_chunk_overlap PASSED
tests/unit/test_embedding_service.py::test_generate_embedding PASSED
tests/unit/test_validators.py::test_sanitize_input PASSED

========== 12 passed in 2.43s ==========
```

### Backend Integration Tests

**Note**: Integration tests require backend server to be running.

```bash
cd backend
pytest tests/integration/ -v
```

**Expected output**:
```
tests/integration/test_chat_endpoint.py::test_chat_basic_query PASSED
tests/integration/test_chat_endpoint.py::test_chat_with_selected_text PASSED
tests/integration/test_vector_search.py::test_search_similar PASSED

========== 8 passed in 5.12s ==========
```

### Frontend Tests

```bash
# From project root
npm test
```

---

## Common Issues and Solutions

### Issue 1: `Collection 'book_content' already exists`

**Cause**: Running `setup_qdrant.py` multiple times

**Solution**:
```bash
python scripts/setup_qdrant.py --force-recreate
```

Or delete collection manually in Qdrant Cloud dashboard.

---

### Issue 2: `OPENAI_API_KEY not found`

**Cause**: `.env` file missing or not loaded

**Solutions**:
1. Verify `.env` exists in backend directory:
   ```bash
   ls backend/.env
   ```

2. Check `.env` contains the key:
   ```bash
   grep OPENAI_API_KEY backend/.env
   ```

3. If missing, copy from project root:
   ```bash
   cp .env backend/.env
   ```

---

### Issue 3: Chat widget not appearing

**Cause**: ChatKit not properly configured or Root.js missing

**Solutions**:

1. **Check ChatKit installation**:
   ```bash
   npm list @openai/chatkit-js
   ```

2. **Verify Root.js exists**:
   ```bash
   ls src/theme/Root.js
   ```

3. **Check browser console** for errors (F12 → Console tab)

4. **Clear npm cache and reinstall**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

---

### Issue 4: `Connection refused` to backend

**Cause**: Backend server not running or wrong port

**Solutions**:

1. **Verify backend is running**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check backend logs** in terminal where `uvicorn` is running

3. **Verify port 8000 is free**:
   ```bash
   lsof -i :8000  # Linux/Mac
   netstat -ano | findstr :8000  # Windows
   ```

4. **Restart backend**:
   ```bash
   # Kill existing process
   pkill -f uvicorn
   # Start again
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

### Issue 5: Slow embedding generation (> 5 minutes)

**Cause**: OpenAI API rate limits or network issues

**Solutions**:

1. **Check OpenAI API status**: https://status.openai.com/

2. **Reduce batch size** in `embed_content.py`:
   - Edit line: `BATCH_SIZE = 10` (default: 50)
   - Run again: `python scripts/embed_content.py`

3. **Resume from interruption**:
   - Script automatically skips already-embedded chunks
   - Just re-run: `python scripts/embed_content.py`

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for embeddings and chat | `sk-proj-abc123...` |
| `QDRANT_URL` | ✅ Yes | Qdrant Cloud cluster URL | `https://xyz.qdrant.io` |
| `QDRANT_API_KEY` | ✅ Yes | Qdrant API key | `abc123xyz...` |
| `NEON_DATABASE_URL` | ✅ Yes | Neon Postgres connection string | `postgresql://user:pass@host/db` |
| `REACT_APP_API_URL` | No | Backend API URL (defaults to localhost) | `http://localhost:8000` |

---

## Next Steps

After completing setup:

1. **Review Implementation Tasks**: See `specs/002-rag-chatbot/tasks.md` for development task breakdown

2. **Read API Documentation**: Check `specs/002-rag-chatbot/contracts/` for full API specs

3. **Explore Codebase**:
   - Backend: `backend/src/` (services, models, API routes)
   - Frontend: `src/components/ChatWidget/` (chat UI components)

4. **Deployment**: See `backend/README.md` for Railway deployment instructions

---

## Quick Reference

**Backend commands** (from `backend/` directory):
```bash
# Start server
uvicorn src.main:app --reload

# Run unit tests
pytest tests/unit/ -v

# Re-embed content after course updates
python scripts/embed_content.py

# Check Qdrant collection stats
python scripts/check_collection.py
```

**Frontend commands** (from project root):
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

**Useful curl commands**:
```bash
# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user1","message":"What is ROS 2?","session_id":"sess1"}'

# Get chat history
curl "http://localhost:8000/history?session_id=sess1"

# Health check
curl http://localhost:8000/health
```

---

## Support

**Documentation**:
- Spec: `specs/002-rag-chatbot/spec.md`
- Plan: `specs/002-rag-chatbot/plan.md`
- Data Model: `specs/002-rag-chatbot/data-model.md`
- API Contracts: `specs/002-rag-chatbot/contracts/`

**Need help?** Review the Common Issues section above or check backend logs for error details.
