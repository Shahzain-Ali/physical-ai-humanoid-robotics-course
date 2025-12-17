# Implementation Plan: RAG Chatbot Integration

**Branch**: `002-rag-chatbot` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-rag-chatbot/spec.md`

## Summary

Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published Physical AI & Humanoid Robotics course book. The chatbot will enable users to ask natural language questions about course content and receive contextual, cited answers. Key features include semantic search over course material, text selection queries, chat history persistence, and streaming responses.

**Technical Approach**:
- **Backend**: FastAPI REST API with OpenAI Agent SDK for LLM orchestration and automatic Postgres session management
- **Frontend**: React-based ChatKit SDK widget embedded in Docusaurus site
- **Vector Storage**: Qdrant Cloud for course content embeddings and semantic search
- **Database**: Neon Serverless Postgres for chat history (auto-managed by OpenAI Agent SDK's SQLAlchemySession)
- **Embeddings**: OpenAI `text-embedding-3-small` (1536 dimensions)

## Technical Context

**Language/Version**:
- Backend: Python 3.10+
- Frontend: JavaScript/React (Docusaurus 2.x compatible)

**Primary Dependencies**:
- Backend: FastAPI, OpenAI Python SDK (with Agent SDK), Qdrant Client, SQLAlchemy
- Frontend: ChatKit SDK (@openai/chatkit-js), React 17+

**Storage**:
- Vector Database: Qdrant Cloud (free tier: 1GB storage)
- Relational Database: Neon Serverless Postgres (free tier: 0.5GB storage, 100 concurrent connections)
- Course Content Source: Markdown files in `docs/` directory

**Testing**:
- Backend: pytest with pytest-asyncio for async endpoint testing
- Frontend: Jest + React Testing Library for component testing
- Integration: Manual testing with Postman/curl for API endpoints

**Target Platform**:
- Backend: Linux server (Railway.app deployment)
- Frontend: Static site on GitHub Pages (already deployed)

**Project Type**: Web application (backend + frontend integration)

**Performance Goals**:
- API response time: <3 seconds for 95% of requests (P95 latency)
- Embedding search: <500ms for Qdrant vector similarity search
- Concurrent users: Support 100 simultaneous users without degradation
- Chat widget load time: <2 seconds on page load

**Constraints**:
- Must stay within free tier limits (Qdrant: 1GB, Neon: 0.5GB, Railway: 500 hours/month)
- No user authentication required (session-based only)
- Course content in English only
- Mobile-responsive design required

**Scale/Scope**:
- Course content: ~50 pages, ~50,000 words total
- Estimated chunks: ~5,000 content segments (500-1000 tokens each)
- Estimated storage: ~30MB embeddings in Qdrant
- Expected users: 50-200 concurrent course participants during hackathon

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development (SDD)
- ✅ **PASS**: Specification created and validated (`specs/002-rag-chatbot/spec.md`)
- ✅ **PASS**: All user stories prioritized with independent test criteria
- ✅ **PASS**: Functional requirements clearly defined (FR-001 through FR-018)
- ✅ **PASS**: Success criteria measurable and technology-agnostic

### Accuracy and Verification
- ✅ **PASS**: Chatbot will cite source pages for all information (FR-005, FR-006)
- ✅ **PASS**: Responses generated from course content only, not general knowledge (FR-004)
- ✅ **PASS**: Primary sources are course Markdown files in `docs/` directory

### Clarity and Accessibility
- ✅ **PASS**: Chat interface designed for course participants (undergraduates)
- ✅ **PASS**: Error messages user-friendly, no technical jargon (FR-013)
- ✅ **PASS**: Mobile-responsive design for accessibility (FR-016)

### Reproducibility and Traceability
- ✅ **PASS**: All course content sources traceable via citations
- ✅ **PASS**: Implementation will follow Spec-Kit Plus methodology (spec → plan → tasks → implementation)

### Citation and Attribution Standards
- ✅ **PASS**: Chatbot responses will include clickable source citations (FR-006)
- ✅ **PASS**: Citations will reference specific course pages and sections (FR-005)

### Zero-Tolerance Plagiarism Policy
- ✅ **PASS**: Chatbot synthesizes information from course content, does not copy verbatim
- ✅ **PASS**: All responses cite original course sources

### Strict Naming and Technical Conventions
- ✅ **PASS**: All backend files will use snake_case (Python convention)
- ✅ **PASS**: All frontend files will follow Docusaurus conventions (kebab-case for directories)
- ✅ **PASS**: Feature branch named `002-rag-chatbot` (kebab-case)

**Overall Constitution Compliance**: ✅ **PASS** - No violations detected. Feature aligns with all constitutional principles.

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: technology decisions and patterns
├── data-model.md        # Phase 1 output: entity definitions and relationships
├── quickstart.md        # Phase 1 output: developer setup and testing guide
├── contracts/           # Phase 1 output: API contracts (OpenAPI specs)
│   ├── chat-api.yaml    # POST /chat endpoint contract
│   └── history-api.yaml # GET /history endpoint contract
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Backend Structure
backend/
├── src/
│   ├── main.py                      # FastAPI app entry point
│   ├── config.py                    # Environment config (loads .env)
│   │
│   ├── models/
│   │   └── schemas.py               # Pydantic models
│   │       - ChatRequest            # POST /chat request model
│   │       - ChatResponse           # POST /chat response model
│   │       - HistoryRequest         # GET /history query params
│   │       - HistoryResponse        # GET /history response model
│   │       - SourceCitation         # Citation object model
│   │
│   ├── services/
│   │   ├── agent_service.py         # OpenAI Agent SDK wrapper
│   │   │   - AgentService class
│   │   │   - get_or_create_session()
│   │   │   - query() method
│   │   │
│   │   ├── vector_service.py        # Qdrant operations
│   │   │   - VectorService class
│   │   │   - search_similar()
│   │   │   - add_documents()
│   │   │   - create_collection()
│   │   │
│   │   └── embedding_service.py     # Embedding generation
│   │       - EmbeddingService class
│   │       - generate_embedding()
│   │       - batch_generate()
│   │
│   ├── api/
│   │   ├── chat.py                  # /chat endpoint router
│   │   │   - POST /chat handler
│   │   │   - build_context()
│   │   │   - extract_sources()
│   │   │
│   │   └── history.py               # /history endpoint router
│   │       - GET /history handler
│   │       - format_messages()
│   │
│   └── utils/
│       ├── chunker.py               # Content chunking logic
│       │   - chunk_markdown()
│       │   - split_by_headers()
│       │   - calculate_overlap()
│       │
│       └── validators.py            # Input validation
│           - sanitize_input()
│           - validate_query_length()
│
├── scripts/
│   ├── setup_qdrant.py              # One-time: Create Qdrant collection
│   └── embed_content.py             # One-time: Embed all course content
│
├── tests/
│   ├── unit/
│   │   ├── test_chunker.py
│   │   ├── test_embedding_service.py
│   │   └── test_validators.py
│   │
│   └── integration/
│       ├── test_chat_endpoint.py
│       └── test_vector_search.py
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # Backend setup instructions

# Frontend Structure
src/
├── components/
│   └── ChatWidget/
│       ├── index.js                 # Main ChatKit integration
│       ├── ChatWidget.css           # Chat styling
│       ├── SelectionHandler.js      # Text selection logic
│       └── config.js                # API endpoint config
│
└── theme/
    └── Root.js                      # Global wrapper for chat widget

# Deployment Configuration
railway.toml                         # Railway deployment config (backend)
.github/workflows/
└── deploy.yml                       # GitHub Pages deployment (frontend, already exists)
```

**Structure Decision**: Web application structure selected because feature requires both backend API (FastAPI) and frontend integration (Docusaurus). Backend handles AI orchestration, vector search, and database persistence. Frontend embeds chat widget and handles user interactions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations detected. All architectural decisions align with constitutional principles:

- **Single purpose**: Each service has clear responsibility (agent, vector, embedding)
- **Simplicity**: Using managed services (Qdrant Cloud, Neon, Railway) instead of self-hosting infrastructure
- **Standard patterns**: REST API, standard Python project structure, React component integration

---

## Phase 0: Research & Technology Decisions

### Research Questions

1. **OpenAI Agent SDK Integration**: How to properly use `SQLAlchemySession` for automatic Postgres management?
2. **ChatKit SDK Setup**: What are the ChatKit React component requirements and configuration?
3. **Content Chunking Strategy**: What chunk size and overlap maximize retrieval accuracy for technical course content?
4. **Qdrant Collection Configuration**: What distance metric and indexing params optimize semantic search?
5. **Streaming Responses**: How to implement Server-Sent Events (SSE) with FastAPI for streaming?

### Research Tasks

**Task 1: OpenAI Agent SDK - SQLAlchemySession Pattern**
- **Question**: How to configure SQLAlchemySession with Neon Postgres for automatic session management?
- **Sources to investigate**:
  - OpenAI Agent SDK documentation (via Context7: `/openai/swarm`)
  - SQLAlchemy async patterns for connection pooling
- **Deliverable**: Code example in `research.md` showing session initialization and agent creation

**Task 2: ChatKit SDK Integration in Docusaurus**
- **Question**: How to embed ChatKit React component in Docusaurus without breaking SSR (Server-Side Rendering)?
- **Sources to investigate**:
  - ChatKit SDK documentation (via Context7: `/openai/chatkit-js`)
  - Docusaurus theme customization docs (Root.js wrapper pattern)
- **Deliverable**: Integration pattern in `research.md` with SSR considerations

**Task 3: RAG Chunking Strategy for Technical Content**
- **Question**: What chunking approach balances context preservation with retrieval precision for technical course material?
- **Sources to investigate**:
  - LangChain chunking patterns for Markdown
  - Research on optimal chunk sizes for RAG systems (500-1000 tokens commonly cited)
- **Deliverable**: Chunking algorithm specification in `research.md` with token size justification

**Task 4: Qdrant Configuration for Educational Content**
- **Question**: What Qdrant collection settings optimize semantic search for Q&A over course chapters?
- **Sources to investigate**:
  - Qdrant documentation on distance metrics (Cosine vs Euclidean vs Dot Product)
  - Indexing strategies (HNSW parameters for 1536-dim vectors)
- **Deliverable**: Qdrant collection config in `research.md` with parameter justification

**Task 5: Streaming Response Implementation**
- **Question**: How to implement Server-Sent Events (SSE) with FastAPI for streaming OpenAI responses?
- **Sources to investigate**:
  - FastAPI StreamingResponse documentation
  - OpenAI streaming API patterns
- **Deliverable**: Streaming endpoint pattern in `research.md` with error handling

### Expected Outcomes (`research.md`)

**File**: `specs/002-rag-chatbot/research.md`

**Format**:
```markdown
# Research: RAG Chatbot Technology Decisions

## Decision 1: OpenAI Agent SDK with SQLAlchemySession
**Chosen**: Use OpenAI Agent SDK's built-in SQLAlchemySession.from_url()
**Rationale**: Automatic table creation, session management, token tracking without manual SQL
**Alternatives Considered**:
- Manual psycopg2 with custom schema (rejected: more code, more bugs)
- SQLAlchemy Core without Agent SDK (rejected: no built-in conversation management)
**Code Example**: [Paste working initialization code]

## Decision 2: ChatKit SDK Integration Pattern
**Chosen**: Use official @openai/chatkit-js with Docusaurus Root.js wrapper and context7 access
**Rationale**: Official OpenAI SDK with proper SSR handling, context7 integration
**Alternatives Considered**:
- Direct component import (rejected: breaks SSR)
- iframe embed (rejected: poor UX, no shared state)
- Custom implementation (rejected: ChatKit SDK available via context7)
**Integration Pattern**: [Paste Root.js example]

## Decision 3: Content Chunking Strategy
**Chosen**: 500-1000 token chunks with 100 token overlap, split by Markdown headers
**Rationale**: Balances context preservation (overlap) with precision (smaller chunks)
**Alternatives Considered**:
- Fixed 512 tokens (rejected: breaks mid-sentence in technical content)
- No overlap (rejected: loses context at boundaries)
**Algorithm**: [Pseudo-code for chunking logic]

## Decision 4: Qdrant Collection Configuration
**Chosen**: Cosine distance, HNSW indexing with m=16, ef_construct=100
**Rationale**: Cosine best for normalized embeddings, HNSW params balance speed/accuracy
**Alternatives Considered**:
- Euclidean distance (rejected: not normalized for OpenAI embeddings)
- Flat index (rejected: too slow for 5k vectors)
**Configuration**: [Paste collection creation code]

## Decision 5: Streaming Response Pattern
**Chosen**: FastAPI StreamingResponse with async generator
**Rationale**: Standard SSE pattern, compatible with ChatKit streaming display
**Alternatives Considered**:
- WebSockets (rejected: overkill for one-way streaming)
- Polling (rejected: poor UX, wasted requests)
**Implementation**: [Paste streaming endpoint example]
```

---

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

**File**: `specs/002-rag-chatbot/data-model.md`

#### Entity 1: Chat Session
**Description**: Represents a conversation between a user and the chatbot. Managed by OpenAI Agent SDK's SQLAlchemySession.

**Auto-Generated Fields** (by SQLAlchemySession):
- `id` (UUID, primary key)
- `user_id` (String, indexed)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)
- `metadata` (JSON) - stores session context

**Validation Rules**:
- `user_id` must be non-empty string
- Sessions auto-expire after 90 days of inactivity (handled by retention policy)

**State Transitions**: N/A (sessions are created and persisted automatically)

---

#### Entity 2: Chat Message
**Description**: Represents a single message in a conversation. Managed by OpenAI Agent SDK's SQLAlchemySession.

**Auto-Generated Fields** (by SQLAlchemySession):
- `id` (UUID, primary key)
- `session_id` (UUID, foreign key to Session)
- `role` (String: "user" | "assistant")
- `content` (Text)
- `created_at` (Timestamp)
- `metadata` (JSON) - stores selected_text if applicable

**Validation Rules**:
- `role` must be either "user" or "assistant"
- `content` must be 1-10,000 characters
- `session_id` must reference existing session

**Relationships**:
- Belongs to one Chat Session
- Sessions can have many Messages (1:N relationship)

---

#### Entity 3: Course Content Chunk
**Description**: Represents a segment of course material stored in Qdrant for retrieval.

**Fields** (stored as Qdrant payload):
- `chunk_id` (String, unique) - Format: `{page}#{chunk_index}`
- `text` (String) - The actual content chunk
- `embedding` (Vector[1536]) - OpenAI embedding vector
- `page` (String) - Source Markdown file (e.g., "03-ros2.md")
- `section` (String) - Markdown header title
- `url` (String) - Full course URL with anchor (e.g., "/docs/03-ros2#understanding-nodes")
- `chunk_index` (Integer) - Position in page (0-based)
- `token_count` (Integer) - Approximate tokens in chunk

**Validation Rules**:
- `text` must be 50-2000 tokens
- `embedding` must be exactly 1536 dimensions
- `page` must match existing course file
- `url` must be valid course route

**Indexing**:
- Primary index: Vector similarity (HNSW)
- Secondary index: `page` for filtering by source

---

#### Entity 4: Source Citation
**Description**: Reference to course material included in a chatbot response. Ephemeral (not stored, generated per response).

**Fields** (Pydantic model):
- `page` (String) - Source file name
- `section` (String) - Markdown section title
- `url` (String) - Full URL with anchor
- `relevance_score` (Float) - Qdrant similarity score (0-1)

**Validation Rules**:
- `url` must be valid HTTP URL
- `relevance_score` must be 0.0-1.0

**Usage**: Included in ChatResponse to show users where information came from

---

### API Contracts (`contracts/`)

**File 1**: `specs/002-rag-chatbot/contracts/chat-api.yaml`

```yaml
openapi: 3.0.0
info:
  title: RAG Chatbot API
  version: 1.0.0
  description: REST API for Physical AI course chatbot

servers:
  - url: https://physical-ai-backend.railway.app
    description: Production backend

paths:
  /chat:
    post:
      summary: Send a chat message and receive AI response
      operationId: sendChatMessage
      tags:
        - Chat
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - user_id
                - message
                - session_id
              properties:
                user_id:
                  type: string
                  description: Unique identifier for the user (browser session ID)
                  example: "user_abc123"
                message:
                  type: string
                  minLength: 1
                  maxLength: 2000
                  description: User's question about course content
                  example: "What are ROS 2 nodes?"
                selected_text:
                  type: string
                  nullable: true
                  description: Text selected by user before asking (optional)
                  example: "ROS 2 uses a distributed architecture..."
                session_id:
                  type: string
                  description: Unique identifier for the conversation session
                  example: "session_xyz789"
      responses:
        '200':
          description: Successful response with AI-generated answer
          content:
            application/json:
              schema:
                type: object
                required:
                  - response
                  - sources
                  - session_id
                properties:
                  response:
                    type: string
                    description: AI-generated answer to user's question
                    example: "ROS 2 nodes are independent processes that perform computation. Each node can publish and subscribe to topics..."
                  sources:
                    type: array
                    description: Course pages cited in the response
                    items:
                      type: object
                      required:
                        - page
                        - section
                        - url
                      properties:
                        page:
                          type: string
                          example: "03-ros2.md"
                        section:
                          type: string
                          example: "Understanding Nodes"
                        url:
                          type: string
                          format: uri
                          example: "/docs/03-ros2#understanding-nodes"
                        relevance_score:
                          type: number
                          format: float
                          minimum: 0.0
                          maximum: 1.0
                          example: 0.89
                  session_id:
                    type: string
                    example: "session_xyz789"
        '400':
          description: Bad request (invalid input)
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Message exceeds 2000 character limit"
        '429':
          description: Rate limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Too many requests. Please try again in 60 seconds."
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "An error occurred processing your request. Please try again."

  /health:
    get:
      summary: Health check endpoint
      operationId: healthCheck
      tags:
        - System
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "ok"
                  timestamp:
                    type: string
                    format: date-time
```

**File 2**: `specs/002-rag-chatbot/contracts/history-api.yaml`

```yaml
openapi: 3.0.0
info:
  title: Chat History API
  version: 1.0.0

paths:
  /history:
    get:
      summary: Retrieve chat history for a session
      operationId: getChatHistory
      tags:
        - Chat
      parameters:
        - name: session_id
          in: query
          required: true
          schema:
            type: string
          description: Session identifier to retrieve history for
          example: "session_xyz789"
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 50
          description: Maximum number of messages to return
      responses:
        '200':
          description: Chat history retrieved successfully
          content:
            application/json:
              schema:
                type: object
                required:
                  - messages
                  - session_id
                properties:
                  messages:
                    type: array
                    items:
                      type: object
                      required:
                        - role
                        - content
                        - timestamp
                      properties:
                        role:
                          type: string
                          enum: [user, assistant]
                          example: "user"
                        content:
                          type: string
                          example: "What are ROS 2 nodes?"
                        timestamp:
                          type: string
                          format: date-time
                          example: "2025-12-17T10:30:00Z"
                        metadata:
                          type: object
                          nullable: true
                          description: Optional metadata (e.g., selected_text)
                  session_id:
                    type: string
                    example: "session_xyz789"
        '404':
          description: Session not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Session not found"
```

---

### Developer Quickstart (`quickstart.md`)

**File**: `specs/002-rag-chatbot/quickstart.md`

```markdown
# RAG Chatbot - Developer Quickstart

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git
- API Keys (in `.env` file):
  - `OPENAI_API_KEY`
  - `QDRANT_URL` and `QDRANT_API_KEY`
  - `NEON_DATABASE_URL`

## Backend Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys (already done if using project .env)
```

### 3. Initialize Qdrant Collection

```bash
python scripts/setup_qdrant.py
# Output: "Collection 'book_content' created successfully"
```

### 4. Embed Course Content

```bash
python scripts/embed_content.py
# Output: "Embedded 4,832 chunks from 47 course pages"
# This takes ~2-3 minutes
```

### 5. Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# Server running at http://localhost:8000
```

### 6. Test Backend

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "What are ROS 2 nodes?",
    "session_id": "test_session"
  }'
```

**Expected Response**:
```json
{
  "response": "ROS 2 nodes are independent processes...",
  "sources": [
    {
      "page": "03-ros2.md",
      "section": "Understanding Nodes",
      "url": "/docs/03-ros2#understanding-nodes"
    }
  ],
  "session_id": "test_session"
}
```

## Frontend Setup (3 minutes)

### 1. Install ChatKit SDK

```bash
# From project root
npm install @openai/chatkit-js
```

### 2. Configure API Endpoint

Edit `docusaurus.config.js`:
```javascript
customFields: {
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000'
}
```

### 3. Start Docusaurus

```bash
npm start
# Site running at http://localhost:3000
```

### 4. Test Chat Widget

1. Open http://localhost:3000
2. Click floating chat button (bottom-right)
3. Type: "What is NVIDIA Isaac?"
4. Verify response appears with source citations

## Running Tests

### Backend Unit Tests

```bash
cd backend
pytest tests/unit/ -v
```

### Backend Integration Tests

```bash
pytest tests/integration/ -v
```

### Frontend Tests

```bash
npm test
```

## Common Issues

**Issue**: `Collection 'book_content' already exists`
**Fix**: Delete existing collection in Qdrant dashboard or run `python scripts/setup_qdrant.py --force-recreate`

**Issue**: `OPENAI_API_KEY not found`
**Fix**: Ensure `.env` file exists in backend directory and contains valid API key

**Issue**: Chat widget not appearing
**Fix**: Check browser console for errors. Ensure `Root.js` is properly configured in `src/theme/`

## Next Steps

- Review `specs/002-rag-chatbot/tasks.md` for implementation task breakdown
- See `backend/README.md` for deployment instructions
- Check `specs/002-rag-chatbot/contracts/` for full API documentation
```

---

### Agent Context Update

```bash
.specify/scripts/bash/update-agent-context.sh claude
```

**Purpose**: Update `.claude/memory/agent-context.md` (or similar) with new technologies from this plan:
- OpenAI Agent SDK (Python)
- ChatKit SDK (@openai/chatkit-js)
- FastAPI
- Qdrant Client
- Neon Postgres (via SQLAlchemySession)

**Expected Output**: "Agent context updated with 5 new technologies"

---

## Post-Phase 1 Constitution Re-Check

### Spec-Driven Development (SDD)
- ✅ **PASS**: Design artifacts created (research.md, data-model.md, contracts/, quickstart.md)
- ✅ **PASS**: All NEEDS CLARIFICATION items resolved in research.md

### Accuracy and Verification
- ✅ **PASS**: API contracts specify citation fields in all responses
- ✅ **PASS**: Data model includes Source Citation entity for attribution

### Clarity and Accessibility
- ✅ **PASS**: Quickstart guide provides clear setup instructions
- ✅ **PASS**: API error responses use user-friendly messages

### Reproducibility and Traceability
- ✅ **PASS**: All API endpoints documented with OpenAPI specs
- ✅ **PASS**: Setup scripts (setup_qdrant.py, embed_content.py) enable reproduction

### Citation and Attribution Standards
- ✅ **PASS**: Every response includes Source Citation array
- ✅ **PASS**: Citations link directly to course sections

### Zero-Tolerance Plagiarism Policy
- ✅ **PASS**: Chatbot synthesizes information, does not copy course text verbatim
- ✅ **PASS**: All responses cite original course sources

### Strict Naming and Technical Conventions
- ✅ **PASS**: Backend files use snake_case (Python convention)
- ✅ **PASS**: Frontend files use kebab-case (Docusaurus convention)
- ✅ **PASS**: All directory names follow established patterns

**Post-Design Constitution Compliance**: ✅ **PASS** - All gates remain green after Phase 1 design.

---

## Summary of Deliverables

**Phase 0 Outputs**:
- ✅ `specs/002-rag-chatbot/research.md` - Technology decisions and rationale

**Phase 1 Outputs**:
- ✅ `specs/002-rag-chatbot/data-model.md` - Entity definitions and relationships
- ✅ `specs/002-rag-chatbot/contracts/chat-api.yaml` - POST /chat OpenAPI spec
- ✅ `specs/002-rag-chatbot/contracts/history-api.yaml` - GET /history OpenAPI spec
- ✅ `specs/002-rag-chatbot/quickstart.md` - Developer setup guide
- ✅ Agent context updated with new technologies

**Phase 2 (Next Step)**:
- Run `/sp.tasks` to generate `specs/002-rag-chatbot/tasks.md` with implementation breakdown

---

## Branch and File Status

**Branch**: `002-rag-chatbot`
**Implementation Plan**: `/mnt/d/Gemini-Cli-Whole-Work/physical-ai-humanoid-robotics-course/specs/002-rag-chatbot/plan.md`

**Next Command**: `/sp.tasks` to generate testable task list for implementation.
