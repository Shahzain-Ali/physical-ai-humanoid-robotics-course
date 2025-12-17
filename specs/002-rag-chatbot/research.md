# Research: RAG Chatbot Technology Decisions

## Decision 1: OpenAI Agent SDK with SQLAlchemySession
**Chosen**: Use OpenAI Agent SDK's built-in SQLAlchemySession.from_url()
**Rationale**: Automatic table creation, session management, token tracking without manual SQL
**Alternatives Considered**:
- Manual psycopg2 with custom schema (rejected: more code, more bugs)
- SQLAlchemy Core without Agent SDK (rejected: no built-in conversation management)
**Code Example**:
```python
from openai import OpenAI
from openai.lib.sqlalchemy_session import SQLAlchemySession

# Initialize OpenAI client
client = OpenAI()

# Initialize SQLAlchemy session for chat history
session = SQLAlchemySession.from_url(
    os.getenv("NEON_DATABASE_URL"),
    create_tables=True  # Automatically creates required tables
)
```

## Decision 2: ChatKit SDK Integration Pattern
**Chosen**: Use official @openai/chatkit-js with Docusaurus Root.js wrapper and context7 access
**Rationale**: Official OpenAI SDK with proper SSR handling, context7 integration
**Alternatives Considered**:
- Direct component import (rejected: breaks SSR)
- iframe embed (rejected: poor UX, no shared state)
- Custom implementation (rejected: ChatKit SDK available via context7)
**Integration Pattern**:
```javascript
// src/components/ChatWidget/index.js
import { ChatKit } from '@openai/chatkit-js';

export default function ChatWidget() {
  // ChatKit integration with Docusaurus SSR handling
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true); // Ensures component only renders on client side
  }, []);

  if (!isClient) {
    return null; // Don't render on server side
  }

  return (
    <ChatKit
      // Configuration with context7 access
      apiUrl={process.env.REACT_APP_API_URL || 'http://localhost:8000'}
      // Additional props...
    />
  );
}
```

## Decision 3: Content Chunking Strategy
**Chosen**: 500-1000 token chunks with 100 token overlap, split by Markdown headers
**Rationale**: Balances context preservation (overlap) with precision (smaller chunks)
**Alternatives Considered**:
- Fixed 512 tokens (rejected: breaks mid-sentence in technical content)
- No overlap (rejected: loses context at boundaries)
**Algorithm**:
```python
def chunk_markdown_file(file_path: str, chunk_size: int = 800, overlap: int = 100):
    """
    Split markdown content intelligently by headers while maintaining token limits
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by H2 and H3 headers first
    header_splits = re.split(r'(\n## |\n### )', content)

    chunks = []
    current_chunk = ""

    for part in header_splits:
        # Calculate tokens for this part
        tokens = len(tiktoken.encoding_for_model("gpt-4").encode(part))

        if tokens > chunk_size:
            # Split large sections further
            sub_chunks = split_large_section(part, chunk_size)
            chunks.extend(sub_chunks)
        elif len(current_chunk) + len(part) < chunk_size:
            current_chunk += part
        else:
            if current_chunk:
                chunks.append(current_chunk)
                # Add overlap from previous chunk
                current_chunk = get_overlap_text(current_chunk, overlap) + part
            else:
                current_chunk = part

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
```

## Decision 4: Qdrant Configuration for Educational Content
**Chosen**: Cosine distance with HNSW indexing (m=16, ef_construct=100)
**Rationale**: Cosine distance works best with normalized embeddings from OpenAI; HNSW provides fast approximate search
**Alternatives Considered**:
- Euclidean distance (rejected: less suitable for high-dimensional embeddings)
- Dot product (rejected: can be skewed by vector magnitude)
**Configuration**:
```python
# Qdrant collection configuration
collection_config = {
    "vectors": {
        "size": 1536,  # OpenAI text-embedding-3-small dimension
        "distance": "Cosine"
    },
    "hnsw_config": {
        "m": 16,           # Max number of edges per node
        "ef_construct": 100,  # Construction time/quality trade-off
        "ef": -1,          # Size of search index (auto-optimized)
        "anonymized_data": False
    },
    "optimizers_config": {
        "memmap_threshold": 20000,    # Use memory mapping for efficiency
        "indexing_threshold": 20000,  # Index vectors in memory
    }
}
```

## Decision 5: Streaming Response Implementation
**Chosen**: Server-Sent Events (SSE) with FastAPI StreamingResponse
**Rationale**: Standard SSE pattern, compatible with ChatKit streaming display, reliable delivery
**Alternatives Considered**:
- WebSockets (rejected: more complex, unnecessary for one-way streaming)
- Long polling (rejected: inefficient, higher server load)
**Implementation**:
```python
from fastapi import Response
from fastapi.responses import StreamingResponse

async def stream_response(user_message: str, session_id: str):
    """Generate streaming response using OpenAI API"""
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )

    async for chunk in response:
        if chunk.choices[0].delta.content:
            yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"

@app.post("/chat/stream")
async def stream_chat(chat_request: ChatRequest):
    return StreamingResponse(
        stream_response(chat_request.message, chat_request.session_id),
        media_type="text/event-stream"
    )
```