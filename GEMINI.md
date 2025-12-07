# GEMINI.md: AI-Powered Robotics Textbook

This document provides a comprehensive overview of the "Physical AI & Humanoid Robotics Textbook" project, its architecture, and development conventions. It is intended to be used as a guide for developers and contributors.

## Project Overview

This project aims to create a definitive, interactive, and AI-powered textbook on Physical AI and Humanoid Robotics. The final product will be a Docusaurus-based website that serves as a comprehensive knowledge base and a platform for practical application through a RAG (Retrieval-Augmented Generation) chatbot.

The project is developed using a strict "Spec-Driven Development" (SDD) methodology, facilitated by a toolset called "SpecKit Plus" and an AI assistant named "Claude Code".

### Architecture

The project is composed of two main components:

*   **Frontend:** A [Docusaurus](https://docusaurus.io/) v3 website that presents the textbook content and provides the user interface for the RAG chatbot. The frontend is built with React and Markdown.
*   **Backend:** A [FastAPI](https://fastapi.tiangolo.com/) (Python) application that provides the backend for the RAG functionality. It uses the [Qdrant](https://qdrant.tech/) vector database to store and query embeddings of the textbook content and integrates with either the Gemini or OpenAI APIs to generate responses.

## Building and Running

### Backend (FastAPI)

1.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

2.  **Run the development server:**
    ```bash
    uvicorn backend.app:app --reload
    ```
    *TODO: Verify the exact command to run the FastAPI application.*

### Frontend (Docusaurus)

1.  **Install dependencies:**
    ```bash
    cd frontend/my-book
    npm install
    ```

2.  **Run the development server:**
    ```bash
    npm start
    ```

The Docusaurus development server will typically start on `http://localhost:3000`.

## Development Conventions

This project follows a highly structured and disciplined development process, as defined in the `.specify/memory/constitution.md` file.

### Spec-Driven Development (SDD)

All development work must adhere to the Spec-Driven Development (SDD) methodology:

1.  **Specification (`spec.md`):** All new features or major changes must start with a clear specification.
2.  **Plan (`plan.md`):** An architectural plan is created to detail the implementation.
3.  **Tasks (`tasks.md`):** The work is broken down into testable tasks.

### AI-Assisted Development

The "Claude Code" AI assistant is the primary interface for development tasks, including code generation, refactoring, and documentation.

### Prompt History and Architectural Decisions

*   **Prompt History Records (PHRs):** All significant user interactions and development steps must be recorded as PHRs in the `history/prompts/` directory.
*   **Architectural Decision Records (ADRs):** Significant architectural decisions must be documented as ADRs in the `history/adr/` directory. The AI assistant will suggest when to create an ADR.

### Code Quality and Style

*   **Python:** Follows the PEP 8 style guide. Code is formatted with `black` and linted with `mypy`.
*   **JavaScript/React:** Follows the Airbnb style guide. Code is formatted with `prettier`.
*   **Version Control:** A Gitflow-like branching strategy is used. All work is done on feature branches and merged via pull requests.

### Key Files and Directories

*   `.specify/memory/constitution.md`: The master document outlining the project's principles, architecture, and technology stack.
*   `specs/`: Contains the specifications, plans, and tasks for each feature.
*   `history/`: Contains the Prompt History Records (PHRs) and Architectural Decision Records (ADRs).
*   `backend/`: The FastAPI application.
*   `frontend/my-book/`: The Docusaurus website.
*   `.claude/`: Configuration and prompts for the "Claude Code" AI assistant.
