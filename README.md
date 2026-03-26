# Physical AI & Humanoid Robotics Course Book

An interactive Docusaurus-based course book covering Physical AI and Humanoid Robotics modules with an AI-powered RAG chatbot that can answer questions from the entire book content. Deployable to GitHub Pages with a FastAPI backend on Hugging Face Spaces.

## Overview

This course book provides comprehensive coverage of Physical AI and Humanoid Robotics topics through 7 modules:

1. **Introduction** - Course overview and foundational concepts
2. **The Robotic Nervous System (ROS 2)** - Understanding robot operating systems
3. **The Digital Twin (Gazebo & Unity)** - Simulation and modeling environments
4. **The AI-Robot Brain (NVIDIA Isaac™)** - Perception and decision making
5. **Vision-Language-Action (VLA)** - Multimodal AI systems
6. **Capstone Project** - Autonomous Humanoid implementation
7. **Assessments** - Evaluation and testing materials

### Weekly Breakdown

The course is structured across 13 weeks, with detailed weekly content covering:
- **Weeks 1-2**: Introduction to Physical AI (sensors, perception, embodied intelligence)
- **Weeks 3-5**: ROS 2 Fundamentals (architecture, nodes, topics, services)
- **Weeks 6-7**: Robot Simulation (Gazebo, Unity, digital twins)
- **Weeks 8-10**: NVIDIA Isaac Platform (perception, manipulation, sim-to-real)
- **Weeks 11-12**: Humanoid Robot Development (kinematics, bipedal locomotion)
- **Week 13**: Conversational Robotics (GPT integration, multi-modal interaction)

## AI Chatbot (RAG-Powered)

The course book includes a built-in AI chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions from the entire book content.

### How It Works

1. All course content is chunked and embedded using OpenAI `text-embedding-3-small` model
2. Embeddings are stored in a Qdrant Cloud vector database (`book_content` collection)
3. When a user asks a question, the query is embedded and a semantic search finds the top 5 most relevant chunks
4. The retrieved context is passed to OpenAI GPT-4o-mini (via OpenAI Agents SDK) to generate an accurate, cited answer
5. Chat history is persisted in Neon Serverless Postgres for session continuity

### Chatbot Features

- **Floating Chat Widget** — A chat button on every page that opens an interactive chat window with message history, typing indicators, and source citations linking back to specific course pages
- **Text Selection → Ask AI** — Select any text (10+ characters) on a course page and a "Ask AI" popup appears, letting you ask contextual questions about that specific content
- **Source Citations** — Every AI response includes clickable source citations showing the page, section, and relevance score
- **Session Persistence** — Chat history persists across page navigation within the same browser tab; user identity persists across sessions via localStorage

### Chatbot Architecture

| Component | Technology |
|-----------|------------|
| Frontend | React components (ChatWidget, TextSelectionPopup) embedded in Docusaurus |
| Backend API | FastAPI (async) |
| AI Model | OpenAI GPT-4o-mini via OpenAI Agents SDK |
| Embeddings | OpenAI `text-embedding-3-small` (1536 dimensions) |
| Vector Database | Qdrant Cloud |
| Chat Database | Neon Serverless Postgres (SQLAlchemy + NullPool) |
| Deployment | Hugging Face Spaces (backend), GitHub Pages (frontend) |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Process a question and return AI response with source citations |
| POST | `/api/chat/stream` | Streaming variant of chat endpoint |
| GET | `/api/history?session_id=...` | Retrieve paginated chat history for a session |
| DELETE | `/api/history/{session_id}` | Delete chat history for a session |
| GET | `/health` | Health check |

### Backend Setup

For detailed backend setup instructions (Python environment, API keys, Qdrant initialization, content embedding), see the [Backend README](backend/README.md).

**Quick start:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI, Qdrant, and Neon API keys
python scripts/setup_qdrant.py
python scripts/embed_content.py
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

The site will be available at http://localhost:3000

## Building for Production

To build the static site:

```bash
npm run build
```

The built site will be in the `build/` directory.

## Deployment

The site is configured for GitHub Pages deployment. The deployment settings are in `docusaurus.config.js`.

## Project Structure

```
physical-ai-humanoid-robotics-course/
├── docs/                        # Course content (Markdown files)
│   ├── index.md                 # Introduction / Course Overview (includes weekly breakdown)
│   ├── ros2.md                  # Module 1: The Robotic Nervous System (ROS 2)
│   ├── simulation.md            # Module 2: The Digital Twin (Gazebo & Unity)
│   ├── isaac.md                 # Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   ├── vla.md                   # Module 4: Vision-Language-Action (VLA)
│   ├── capstone.md              # Capstone Project: The Autonomous Humanoid
│   └── assessments.md           # Assessments
├── src/                         # Custom React components and CSS
│   ├── components/
│   │   ├── ChatWidget/          # Floating AI chatbot widget
│   │   │   ├── index.js         # Chat UI with message history & source citations
│   │   │   ├── config.js        # API endpoints, UI, and behavior configuration
│   │   │   └── ChatWidget.css   # Chat widget styling
│   │   └── TextSelectionPopup/  # "Ask AI" popup on text selection
│   │       ├── index.js         # Selection detection & popup logic
│   │       └── TextSelectionPopup.css
│   ├── css/custom.css           # Custom styling
│   └── pages/index.js           # Landing page
├── backend/                     # RAG Chatbot FastAPI backend
│   ├── src/
│   │   ├── main.py              # FastAPI app setup, CORS, routers
│   │   ├── config.py            # Database engine & session config (Neon Postgres)
│   │   ├── api/
│   │   │   ├── chat.py          # POST /api/chat & /api/chat/stream endpoints
│   │   │   └── history.py       # GET/DELETE /api/history endpoints
│   │   ├── models/
│   │   │   ├── database.py      # SQLAlchemy models (ChatSession, ChatMessage)
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── agent_service.py # RAG orchestration (OpenAI Agents SDK)
│   │   │   ├── embedding_service.py # OpenAI embedding generation
│   │   │   └── vector_service.py    # Qdrant semantic search
│   │   └── utils/
│   │       ├── chunker.py       # Content chunking for embeddings
│   │       └── validators.py    # Input validation & sanitization
│   ├── scripts/
│   │   ├── setup_qdrant.py      # Initialize Qdrant collection
│   │   └── embed_content.py     # Process & embed course content
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variables template
├── examples/                    # ROS 2 and Isaac code examples
│   ├── ros2-examples/           # ROS 2 publisher/subscriber examples
│   ├── isaac-examples/          # NVIDIA Isaac perception examples
│   └── simulation-examples/     # Robot controller examples
├── static/                      # Static assets (images, etc.)
├── .github/workflows/
│   └── deploy.yml               # Automated GitHub Pages deployment
├── docusaurus.config.js         # Docusaurus config (includes chatbot API URL)
├── sidebars.js                  # Navigation structure
├── package.json                 # Project dependencies and scripts
└── README.md                    # Project overview
```

## MCP (Model Context Protocol) Setup

This project uses MCP servers for GitHub integration and Context7 documentation. To set up:

1. Copy the example MCP configuration:
   ```bash
   cp .mcp.json.example .mcp.json
   ```

2. Add your API keys to `.mcp.json`:
   - `GITHUB_PERSONAL_ACCESS_TOKEN`: Get from [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
   - `CONTEXT7_API_KEY`: Get from [Context7 Dashboard](https://context7.com)

3. The `.mcp.json` file is gitignored to protect your secrets.

**Note:** Never commit your actual API keys to version control!

## Contributing

To add new content:

1. Create a new Markdown file in the `docs/` directory
2. Add the new page to the navigation by editing `sidebars.js`
3. Build and test the site with `npm run build` and `npm run serve`

## License

This project is licensed under the MIT License.