# Feature Specification: RAG Chatbot Integration

**Feature Branch**: `002-rag-chatbot`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published book. The chatbot will use the OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud (Free Tier). It must answer user questions about the book's content, including answering questions based only on user-selected text."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Course Content (Priority: P1)

As a course participant, I want to ask questions about the Physical AI & Humanoid Robotics course material and receive accurate answers with source citations, so I can quickly find information without manually searching through all course pages.

**Why this priority**: This is the core value proposition of the chatbot - enabling users to get instant, contextual answers to their questions. Without this, the chatbot has no purpose.

**Independent Test**: Can be fully tested by opening any course page, clicking the chat widget, typing a question like "What are ROS 2 nodes?", and verifying the response includes relevant content from the course with citations to specific pages.

**Acceptance Scenarios**:

1. **Given** user is on any course page, **When** user clicks the floating chat button, **Then** chat panel opens showing empty conversation
2. **Given** chat panel is open, **When** user types "What is NVIDIA Isaac?" and clicks send, **Then** chatbot responds with relevant information from the course about NVIDIA Isaac and cites the source page (e.g., "05-isaac.md")
3. **Given** user asks a question, **When** chatbot generates response, **Then** response includes clickable links to the cited course sections
4. **Given** user asks a general course question, **When** multiple course sections are relevant, **Then** chatbot synthesizes information from top 3-5 most relevant sections and lists all sources

---

### User Story 2 - Ask Questions About Selected Text (Priority: P2)

As a course participant, I want to highlight specific text on a course page and ask questions about that exact content, so I can get targeted clarification without the chatbot searching the entire course.

**Why this priority**: This enhances the core chatbot experience by providing contextual queries. It's a powerful feature but not essential for MVP - users can still copy-paste text into their questions.

**Independent Test**: Can be tested by selecting a paragraph about "ROS 2 topics" on the ROS 2 page, clicking the "Ask about this" tooltip that appears, and verifying the chatbot's response focuses specifically on the selected text.

**Acceptance Scenarios**:

1. **Given** user is reading a course page, **When** user highlights any text (>10 characters), **Then** an "Ask about this" tooltip appears near the selection
2. **Given** tooltip is visible, **When** user clicks "Ask about this", **Then** chat widget opens with the selected text pre-filled as context
3. **Given** selected text is included in query, **When** chatbot generates response, **Then** response prioritizes the selected text as primary context over general course search
4. **Given** user has selected text, **When** user types a question in the chat, **Then** question is answered specifically in relation to the selected text

---

### User Story 3 - Persist Chat History Across Sessions (Priority: P3)

As a course participant, I want my chat history to be saved so I can return later and review previous questions and answers, enabling continuous learning across multiple study sessions.

**Why this priority**: This improves user experience by allowing review of past conversations, but the chatbot provides value even without persistence. Users can still ask questions in each new session.

**Independent Test**: Can be tested by asking 3 questions in a chat session, closing the browser, reopening the course site an hour later, and verifying all 3 previous messages are still visible in the chat history.

**Acceptance Scenarios**:

1. **Given** user has asked 3 questions in current session, **When** user navigates to a different course page, **Then** chat history shows all previous messages
2. **Given** user has a chat session with 5 messages, **When** user closes browser and returns 1 hour later, **Then** previous chat history is restored and visible
3. **Given** user has multiple chat sessions over several days, **When** user opens chat widget, **Then** all historical conversations are accessible (with session timestamps)
4. **Given** user has a long chat history (>20 messages), **When** user scrolls up in chat panel, **Then** older messages load smoothly without performance degradation

---

### User Story 4 - Receive Fast, Streaming Responses (Priority: P2)

As a course participant, I want to see the chatbot's response appear progressively as it's being generated, so I get immediate feedback and don't wait for the full response before seeing anything.

**Why this priority**: Streaming responses significantly improve perceived performance and user experience, making the chatbot feel responsive even for longer answers.

**Independent Test**: Can be tested by asking a complex question that generates a long response, and verifying text appears word-by-word in real-time rather than all at once after a delay.

**Acceptance Scenarios**:

1. **Given** user sends a question, **When** chatbot begins generating response, **Then** typing indicator appears immediately (within 500ms)
2. **Given** chatbot is generating a response, **When** first words are available, **Then** they appear in the chat panel while rest of response continues generating
3. **Given** response is streaming, **When** user scrolls chat panel, **Then** auto-scroll keeps latest text visible unless user manually scrolls up
4. **Given** long response is streaming, **When** network connection is lost mid-stream, **Then** partial response is preserved and error message shows "Connection lost - response incomplete"

---

### Edge Cases

- **No relevant content found**: What happens when user asks a question completely unrelated to the course (e.g., "What's the weather today?")? System should respond with "I can only answer questions about the Physical AI & Humanoid Robotics course. Please ask about course topics like ROS 2, NVIDIA Isaac, simulation, or humanoid robotics."

- **Very long questions**: How does system handle queries exceeding 500 characters? System should accept queries up to 2000 characters and gracefully truncate if exceeded.

- **Extremely short queries**: What happens when user sends single-word queries like "Isaac" or "nodes"? System should request clarification: "Could you please provide more context? For example, 'What is NVIDIA Isaac?' or 'Explain ROS 2 nodes'."

- **Rapid successive queries**: How does system handle user sending 5 messages within 10 seconds? System should queue messages and process sequentially, showing appropriate status indicators for each.

- **Special characters and code**: What happens when user pastes code snippets or markdown in questions? System should preserve formatting and treat code as part of the context for answering.

- **Multiple browser tabs**: How does system handle same user having chat open in 3 different browser tabs? Each tab should share the same session and sync history in real-time (or show message to reload if real-time sync not feasible).

- **Network interruptions**: What happens when internet connection drops during query processing? System should show "Reconnecting..." status and retry automatically, or allow manual retry with "Resend message" button.

- **Empty course sections**: How does system respond when asking about course sections that exist in navigation but have minimal content? System should acknowledge the topic and provide whatever limited content exists, noting "This section is still being developed."

- **Concurrent user load**: How does system perform when 50 users are asking questions simultaneously? Response time may increase but should remain under 5 seconds, with graceful degradation rather than errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a floating chat button visible on all course pages (bottom-right corner, non-intrusive to reading experience)

- **FR-002**: System MUST accept natural language text queries from users about course content (minimum 1 character, maximum 2000 characters)

- **FR-003**: System MUST retrieve relevant course content chunks using semantic similarity search before generating responses

- **FR-004**: System MUST generate contextual responses using retrieved course material as primary information source, not general knowledge

- **FR-005**: System MUST cite source pages for all information included in responses (showing page name and section, e.g., "03-ros2.md - Understanding Nodes")

- **FR-006**: System MUST make cited sources clickable links that navigate directly to the relevant course section

- **FR-007**: System MUST support text selection queries by detecting when user highlights text on page and offering "Ask about this" option

- **FR-008**: System MUST prioritize user-selected text as primary context when generating responses to selection-based queries

- **FR-009**: System MUST persist chat history for each user session to database for future retrieval

- **FR-010**: System MUST restore previous chat history when user returns to the course site

- **FR-011**: System MUST display typing indicators while responses are being generated

- **FR-012**: System MUST stream responses progressively (word-by-word) rather than waiting for complete generation

- **FR-013**: System MUST handle errors gracefully with user-friendly messages (no stack traces or technical errors shown to users)

- **FR-014**: System MUST maintain conversation context within a session (user can ask follow-up questions without repeating context)

- **FR-015**: System MUST limit response generation to course content only - declining to answer off-topic questions with appropriate message

- **FR-016**: System MUST support mobile-responsive design (chat widget works on phones and tablets, not just desktop)

- **FR-017**: System MUST provide visual feedback for all user actions (button clicks, message sending, errors) within 200ms

- **FR-018**: System MUST sanitize user input to prevent injection attacks or malicious content

### Key Entities *(include if feature involves data)*

- **User**: Represents a course participant interacting with the chatbot. Identified by unique user_id (generated on first interaction or from browser session). No personal data required.

- **Chat Session**: Represents a conversation between a user and the chatbot. Contains session_id, user_id, creation timestamp, and last activity timestamp. Sessions group related messages.

- **Chat Message**: Represents a single message in a conversation. Contains role (user or assistant), content (message text), timestamp, session_id, and optional metadata (selected_text if applicable).

- **Course Content Chunk**: Represents a segment of course material stored for retrieval. Contains text content, embedding vector (1536 dimensions), source page, section name, URL, chunk index, and token count.

- **Source Citation**: Represents a reference to course material included in a response. Contains page name (e.g., "03-ros2.md"), section name (e.g., "Understanding Nodes"), and URL anchor (e.g., "/docs/03-ros2#understanding-nodes").

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive relevant answers to course-related questions with at least 80% perceived accuracy (based on user feedback mechanism "Was this helpful?")

- **SC-002**: Chatbot responses include source citations to specific course pages 100% of the time when answering content-based questions

- **SC-003**: Chat widget loads and is visible on all course pages within 2 seconds of page load

- **SC-004**: 95% of responses are generated and begin streaming to user within 3 seconds of query submission

- **SC-005**: Chat history persists across sessions for 90 days, allowing users to review previous conversations

- **SC-006**: Text selection feature is detected and offers "Ask about this" option within 500ms of user highlighting content

- **SC-007**: Chat widget is fully functional on mobile devices (phones and tablets) with responsive layout and touch interactions

- **SC-008**: System handles at least 100 concurrent users asking questions without response time exceeding 5 seconds

- **SC-009**: Zero user-visible errors for 95% of queries (errors are caught and shown as friendly messages, not crashes)

- **SC-010**: Users can complete a typical question-answer interaction (ask question → receive response → click source link) in under 30 seconds

### Assumptions

- Users have modern web browsers with JavaScript enabled (Chrome, Firefox, Safari, Edge - last 2 versions)
- Course content exists in Markdown format in `docs/` directory and remains relatively stable (not changing hourly)
- Users have internet connectivity to interact with the chatbot (no offline mode)
- The chatbot is intended for educational assistance, not for grading or assessment purposes
- User queries will be primarily in English (matching course content language)
- Free tier limits of Qdrant Cloud (1GB storage) and Neon Postgres (100 concurrent connections) are sufficient for hackathon/course usage scale
- OpenAI API is available and operational with acceptable response times (<2 seconds for most queries)

### Out of Scope

The following are explicitly NOT included in this feature:

- **Grading or assessment**: Chatbot will not grade assignments, provide scores, or evaluate student work
- **Multi-language support**: Only English queries and responses (course is in English)
- **Voice input/output**: Text-based interaction only, no speech recognition or text-to-speech
- **Image or video questions**: Users cannot upload images or ask questions about video content directly
- **User authentication**: No login required, chatbot works for all visitors (session-based only)
- **User profiles or preferences**: No saved user settings, customization, or profiles
- **Admin dashboard**: No analytics dashboard for instructors to view chatbot usage patterns
- **Email or notification features**: Chatbot does not send emails or push notifications
- **Multi-user collaboration**: Users cannot share chat sessions or collaborate in same conversation
- **Export chat history**: No feature to download or export conversation transcripts
- **Custom chatbot training**: Instructors cannot add custom Q&A pairs or fine-tune responses beyond course content
