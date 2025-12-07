# Feature Specification: Hackathon I: Physical AI & Humanoid Robotics Textbook

**Feature Branch**: `001-book-core`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "create "book-core" --surface agent

We have completed the project constitution. Now create the full project specification for the hackathon book titled:

“Hackathon I: Physical AI & Humanoid Robotics Textbook”

Include:

1. Book Overview (why this book, purpose, scope)
2. Target Audience (students, beginners, robotics enthusiasts)
3. High-Level Table of Contents (10–14 chapters)
4. Functional Requirements:
   - Book must be built using Docusaurus
   - Book must be deployed on GitHub Pages
   - RAG chatbot must be embedded and respond based on book content
   - Chatbot must also answer based on user-selected text only
   - Backend using FastAPI + Qdrant Free Tier
   - OpenAI ChatKit SDK or MCP agents
   - Claude Code Subagents + Skills must be used for reusable intelligence
5. Non-Functional Requirements:
   - High responsiveness
   - Simple UX and clean UI
   - Fast local dev workflow
   - Strong content organization
6. Constraints:
   - Use Gemini via CCR for LLM generation
   - Use Spec-Kit Plus workflow for all development
   - All changes require plan → tasks → implement
7. Deliverables:
   - Book source repo
   - Live deployed book
   - Fully working RAG chatbot
   - Subagents + Skills demos
   - YouTube demo video
8. Success criteria:
   - Book is complete
   - RAG answers correctly
   - CI/CD deployment works
   - Code quality passes Spec-Kit standards

After writing the specification, save it into:
specs/book-core/spec.md"

## Book Overview

This project aims to develop an AI-powered textbook titled "Hackathon I: Physical AI & Humanoid Robotics Textbook." The book will serve as a comprehensive knowledge base, integrating with an interactive RAG (Retrieval Augmented Generation) chatbot. Its purpose is to provide dynamic content interaction and information retrieval for users interested in physical AI and humanoid robotics. The scope includes content creation, platform development, and AI integration for enhanced learning and interaction. The content will maintain a hybrid tone, being both accessible for beginners and comprehensive enough for motivated learners, balancing foundational explanations with practical applications.

## Target Audience

The primary target audience includes:
- Students interested in AI and robotics.
- Beginners in the field looking for foundational knowledge.
- Robotics enthusiasts eager to learn about physical AI and humanoid robotics.

## High-Level Table of Contents (10–14 chapters)

1.  **Introduction to Physical AI and Robotics**
2.  **Fundamentals of Humanoid Robotics**
3.  **Kinematics and Dynamics of Robotic Systems**
4.  **Sensors and Actuators in Robotics**
5.  **Robot Control Systems**
6.  **Machine Learning for Robotics**
7.  **Computer Vision in Robotics**
8.  **Robot Navigation and Path Planning**
9.  **Human-Robot Interaction**
10. **Ethical Considerations in AI and Robotics**
11. **Advanced Topics in Physical AI**
12. **Future Trends in Humanoid Robotics**

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reading Book Content (Priority: P1)

A user wants to read a chapter of the "Hackathon I: Physical AI & Humanoid Robotics Textbook" to learn about a specific topic.

**Why this priority**: Core functionality of a textbook. Without reading content, other features are irrelevant.

**Independent Test**: The book content is accessible and readable in a web browser. A user can navigate between chapters and sections.

**Acceptance Scenarios**:

1.  **Given** a user opens the book URL, **When** they navigate to a chapter, **Then** the chapter content is displayed correctly.
2.  **Given** a user is reading a chapter, **When** they click on a link to another section or chapter, **Then** they are smoothly redirected to the new content.

---

### User Story 2 - Interacting with the RAG Chatbot (Priority: P1)

A user wants to ask questions about the book content and receive accurate answers from the embedded RAG chatbot, which appears as a contextual pop-up. Users will select text by highlighting it, then clicking a specific "Ask Chatbot about this" button within the pop-up. The maximum length for selected text will be 1000 characters.

**Why this priority**: Key innovative feature for interactive learning and information retrieval.

**Independent Test**: A user can highlight a section of text (up to 1000 characters), activate the chatbot pop-up, click the "Ask Chatbot about this" button, and then type a question to receive a relevant and accurate answer based on the selected text and the book's knowledge base.

**Acceptance Scenarios**:

1.  **Given** a user is on any book page and activates the chatbot pop-up, **When** they type a question related to the book content into the chatbot, **Then** the chatbot provides a concise and accurate answer based on the book's knowledge base.
2.  **Given** a user has selected specific text (up to 1000 characters) within the book and activates the chatbot pop-up, **When** they click the "Ask Chatbot about this" button and ask a question to the chatbot, **Then** the chatbot prioritizes its response based on the selected text.

---

### User Story 3 - Exploring with Claude Code Subagents/Skills (Priority: P2)

A developer/researcher wants to use Claude Code Subagents and Skills to explore the book's codebase, understand its architecture, or generate content.

**Why this priority**: Enhances development and content creation workflow, demonstrating the project's advanced AI integration.

**Independent Test**: A user can successfully invoke a Claude Code Subagent or Skill to perform a task related to the project codebase or content.

**Acceptance Scenarios**:

1.  **Given** a user invokes a Claude Code Subagent (e.g., `Explore`), **When** they ask a question about the book's codebase structure, **Then** the subagent provides an accurate overview.
2.  **Given** a user invokes a Claude Code Skill, **When** they request content generation for a new chapter outline, **Then** the skill generates a relevant outline.

---

**User Story: Mandatory Background Survey**
- As a new user, after signing up I must complete a background survey so the system can personalize content.
- Acceptance Criteria:
  - Given a successful signup, the user is redirected to the Background Survey.
  - The user cannot use the "Personalize Content" feature until all required survey fields are completed.
  - The survey results are stored in `user_backgrounds` table in Neon Postgres.

**User Story: Personalize Chapter Content**
- As a logged-in user who completed the survey, I can click "Personalize Content" at the start of any chapter to receive tailored real-life analogies and adjusted technical depth for that chapter.
- Acceptance Criteria:
  - Given completion of the mandatory survey, the "Personalize Content" button is enabled.
  - When clicked, the system returns a version of the chapter customized for the user's `interest_field` and `programming_level`.
  - The chapter customization maintains core learning objectives and does not change assessment questions (only examples/analogies and optional extra examples).
  - A "Translate to Urdu" button is visible at chapter start and returns an Urdu translation when clicked.

**User Story: Data Storage & Privacy**
- As the product owner, user background metadata must be stored securely and not leaked into Qdrant.
- Acceptance Criteria:
  - Background metadata is stored in Neon Postgres only.
  - Qdrant collections remain used only for book content, code snippets, and diagram descriptions.
  - Implement role-based access control for reading/editing user profiles.

## Edge Cases

-   What happens when the RAG chatbot cannot find a relevant answer in the book content? (Should provide a polite "I don't know" or suggest rephrasing.)
-   How does the system handle very long or complex user-selected text for chatbot queries? (Should process efficiently or provide feedback if too long.)
-   What if the Docusaurus build or GitHub Pages deployment fails? (CI/CD should report errors clearly.)
-   What if the Qdrant database is unavailable or the LLM API key is invalid? (Chatbot should gracefully handle errors and inform the user.)

## Requirements *(mandatory)*

### Data Model: Qdrant Collections and Metadata

To support granular RAG queries and efficient retrieval based on content type, Qdrant will utilize multiple collections, each with tailored metadata:

-   **Collection**: `book_text_chunks`
    -   **Description**: Stores vectorized chunks of the book's prose content.
    -   **Metadata**: `chapter_title`, `section_heading`, `page_number`, `source_file`, `text_chunk_id`, `keywords`.

-   **Collection**: `code_snippets`
    -   **Description**: Stores vectorized code examples extracted from the book.
    -   **Metadata**: `chapter_title`, `section_heading`, `language`, `code_example_id`, `keywords`, `description` (of the code).

-   **Collection**: `diagram_descriptions`
    -   **Description**: Stores vectorized textual descriptions or captions for diagrams and figures.
    -   **Metadata**: `chapter_title`, `figure_number`, `description_id`, `keywords`, `alt_text`.

### Neon Postgres Schema (Background Metadata table)
Create table: `user_backgrounds`
Columns:
- `id` BIGSERIAL PRIMARY KEY
- `user_id` UUID NOT NULL REFERENCES users(id)
- `role` VARCHAR(64)
- `programming_level` VARCHAR(32)
- `hardware_specs` TEXT
- `software_experience` TEXT
- `interest_field` VARCHAR(128)
- `preferred_language` VARCHAR(16)
- `goals` TEXT
- `created_at` TIMESTAMP WITH TIME ZONE DEFAULT now()
- `updated_at` TIMESTAMP WITH TIME ZONE DEFAULT now()

Add DB migrations and necessary indices for `user_id` and `interest_field`.

### Qdrant Usage Clarification
- Qdrant collections remain dedicated to book content:
  - `book_text_chunks` (metadata: chapter_title, section_heading, page_number, source_file, text_chunk_id, keywords)
  - `code_snippets` (metadata: chapter_title, section_heading, language, code_example_id, keywords, description)
  - `diagram_descriptions` (metadata: chapter_title, figure_number, description_id, keywords, alt_text)
- DO NOT store user background metadata in Qdrant.

### Neon Postgres Schema (Background Metadata table)
Create table: `user_backgrounds`
Columns:
- `id` BIGSERIAL PRIMARY KEY
- `user_id` UUID NOT NULL REFERENCES users(id)
- `role` VARCHAR(64)
- `programming_level` VARCHAR(32)
- `hardware_specs` TEXT
- `software_experience` TEXT
- `interest_field` VARCHAR(128)
- `preferred_language` VARCHAR(16)
- `goals` TEXT
- `created_at` TIMESTAMP WITH TIME ZONE DEFAULT now()
- `updated_at` TIMESTAMP WITH TIME ZONE DEFAULT now()

Add DB migrations and necessary indices for `user_id` and `interest_field`.

### New Requirements: Auth, Survey & Personalization
- R-Auth-001: Integrate Better-Auth for signup and signin with Email/Password and session management.
- R-Auth-002: Implement OAuth2/JWT support for API access control in the FastAPI backend.
- R-Survey-001: Launch Background Survey immediately after signup as a mandatory step.
- R-Profile-001: Store background metadata in Neon Postgres; do NOT store this data in Qdrant.
- R-Personalize-001: Personalization only activates after mandatory survey completion.
- R-Translate-001: Provide a "Translate to Urdu" button at the start of every chapter.

### Functional Requirements

-   **FR-001**: The book MUST be built using the Docusaurus framework.
-   **FR-002**: The book MUST be deployable on GitHub Pages.
-   **FR-003**: A RAG chatbot MUST be embedded within the book, capable of responding based on the entire book content.
-   **FR-004**: The RAG chatbot MUST also be capable of responding based on user-selected text only.
-   **FR-005**: The backend for the RAG chatbot MUST be implemented using FastAPI.
-   **FR-006**: The vector database for the RAG chatbot MUST utilize Qdrant Cloud (Free Tier).
-   **FR-007**: The LLM interaction for the chatbot MUST use OpenAI ChatKit SDK or MCP agents.
-   **FR-008**: Claude Code Subagents and Skills MUST be integrated to provide reusable intelligence for development and content generation.

### Non-Functional Requirements

-   **NFR-001**: The book and chatbot MUST exhibit high responsiveness (e.g., page loads under 2 seconds, chatbot responses under 5 seconds).
-   **NFR-002**: The user experience (UX) and user interface (UI) MUST be simple, clean, and intuitive.
-   **NFR-003**: The local development workflow MUST be fast and efficient, allowing quick iterations.
-   **NFR-004**: The book content MUST have strong and logical organization, making it easy to navigate and understand.

### FastAPI Endpoints & Security
Add or confirm endpoints:
- `POST /auth/signup` -> Better-Auth backed signup (email/password)
- `POST /auth/signin` -> Session creation / JWT return
- `GET /auth/me` -> Returns current user profile
- `POST /users/{user_id}/background` -> Submit/update survey results (requires auth)
- `GET /users/{user_id}/background` -> Retrieve survey profile (requires auth)
- `POST /personalize/chapter/{chapter_id}` -> Returns personalized chapter content for the user (requires auth)
- `POST /translate/chapter/{chapter_id}` -> Returns Urdu translation for a chapter (requires auth)
- `POST /feedback/personalization` -> User feedback for personalization outputs

Security:
- Use OAuth2/JWT for all protected endpoints.
- Use API key + rate-limiting for public RAG endpoints (if any).
- Require HTTPS and enforce CSRF protections where applicable.

### Constraints

-   **C-001**: LLM generation MUST use Gemini via CCR (Claude Code Red).
-   **C-002**: All development MUST follow the Spec-Kit Plus workflow.
-   **C-003**: All feature implementations MUST adhere to the plan → tasks → implement lifecycle.

## Clarifications

### Session 2025-12-04

- Q: What is the intended tone and depth for the book's content? → A: Hybrid (Accessible yet Comprehensive)
- Q: What is the desired user experience (UX) flow for interacting with the RAG chatbot within the book? → A: Contextual Pop-up
- Q: How should the user select text for the RAG chatbot, and what are the limitations (e.g., maximum length)? → A: Hybrid (Highlight + Button) with a reasonable maximum selection of 1000 characters.
- Q: What is the desired structure for Qdrant collections and what metadata should be stored alongside the vector embeddings for efficient retrieval? → A: Multiple Collections (Categorized)

### Session: Signup, Survey & Personalization
- Q: Which Better-Auth features must be integrated for Signup/Signin?
  - A: Email/Password authentication, full session management (session cookies), device session tracking, magic link (optional), OAuth2/JWT integration for FastAPI security, auto-check for existing accounts, and post-signup redirect to Background Survey.

- Q: What questions must be asked in the Background Survey (post-signup)?
  - A: The Background Survey will include:
    1. Current role (Student / Developer / Engineer / Beginner / Researcher)
    2. Programming experience level (None, Beginner, Intermediate, Advanced)
    3. Hardware setup (Laptop specs / GPU availability / OS)
    4. Software tools experience (Python, ROS2, Gazebo, Unity, Isaac Sim, etc.)
    5. Field of interest (Robotics, AI Agents, Vision, Humanoids, Embedded)
    6. Preferred language (English / Urdu)
    7. Future goals (Career path or specialization)

- Q: Where is user background metadata stored?
  - A: Use Neon Postgres as the authoritative store for background metadata (recommended). Qdrant will NOT store user background metadata.
- Q: How does the Personalization Button behave?
  - A: Clicking "Personalize Content" rewrites or customizes chapter content based on the user profile:
    - Uses the user's selected field to adapt real-life analogies and examples.
    - Adjusts technical depth according to experience level (beginner → simpler analogies; advanced → higher technical depth).
    - Supports a dedicated "Translate to Urdu" button at the start of each chapter that delivers an Urdu translation of the chapter content.

- Q: Are there workflow dependencies between signup, survey, and personalization?
  - A: YES — Personalization is locked until the user completes the Background Survey.

## Deliverables

-   **DL-001**: Complete book source repository.
-   **DL-002**: Live deployed version of the book on GitHub Pages.
-   **DL-003**: Fully working RAG chatbot embedded in the book.
-   **DL-004**: Demos and documentation for integrated Claude Code Subagents and Skills.
-   **DL-005**: YouTube demo video showcasing the project.
- `specs/001-book-core/plan.md`: The detailed implementation plan.
- `specs/001-book-core/tasks.yml`: The generated actionable tasks.
- DB migration SQL for `user_backgrounds` schema (to be generated).
- Example FastAPI route stubs for new endpoints with auth decorators (to be generated).
- Frontend wireframes or notes describing the personalization UX (tooltip, disabled/enabled states, translation toggle) (to be generated).
- Acceptance test cases for mandatory survey and personalization feature (to be generated).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The "Hackathon I: Physical AI & Humanoid Robotics Textbook" is 100% complete with all chapters outlined in the high-level TOC.
-   **SC-002**: The RAG chatbot answers questions based on book content with at least 90% accuracy (verified by user testing).
-   **SC-003**: The CI/CD pipeline for GitHub Pages deployment works flawlessly, deploying updates within 5 minutes of a merge to `main`.
-   **SC-004**: The codebase adheres to Spec-Kit standards, passing all automated code quality checks (e.g., linting, type-checking).
-   **SC-005**: Users can navigate the book and interact with the chatbot with a perceived "high responsiveness" (e.g., <2s page load, <5s chatbot response).
