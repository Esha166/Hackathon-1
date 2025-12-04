<!--
Sync Impact Report:
Version change: 0.0.0 → 0.1.0
List of modified principles: All new
Added sections: All sections as per user request
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .claude/commands/*.md: ⚠ pending
Follow-up TODOs: None
-->
# Project Constitution: Physical AI & Humanoid Robotics Textbook

## 1. Governance

- **RATIFICATION_DATE**: 2025-12-04
- **LAST_AMENDED_DATE**: 2025-12-04
- **CONSTITUTION_VERSION**: 0.1.0
- **AMENDMENT_PROCEDURE**: All amendments require explicit architect approval and must follow semantic versioning. Minor changes (PATCH) can be proposed by any team member. Significant changes (MINOR/MAJOR) require review by at least two senior architects.
- **COMPLIANCE_REVIEW**: Annually, or upon significant architectural shifts, to ensure ongoing alignment and enforceability.

## 2. Project Vision and Long-Term Purpose

To create the definitive, interactive, and AI-powered textbook on Physical AI and Humanoid Robotics, serving as a comprehensive knowledge base and a platform for practical application through a RAG chatbot. Our long-term purpose is to democratize access to advanced robotics education and foster innovation in the field.

## 3. Boundaries of the System

- **IN_SCOPE**: AI-powered interactive textbook content, RAG chatbot for information retrieval, backend services for content ingestion and querying, frontend for content presentation and chatbot interface.
- **OUT_OF_SCOPE**: Real-time control of physical robots, advanced simulation environments beyond conceptual demonstrations, general-purpose chatbot functionality unrelated to textbook content.

## 4. Core Principles

### PRINCIPLE_1: **Spec-Driven Development (SDD)**
- **RULE**: All new features, major changes, and architectural decisions MUST be initiated with a clear specification (`spec.md`) and planned in detail (`plan.md`, `tasks.md`) following SpecKit Plus methodologies.
- **RATIONALE**: Ensures clarity, reduces ambiguity, facilitates early feedback, and maintains alignment across development cycles.

### PRINCIPLE_2: **Modularity and Scalability**
- **RULE**: Codebase MUST be designed with clear separation of concerns. Components and services MUST be loosely coupled, promoting independent development, deployment, and scalability.
- **RATIONALE**: Enhances maintainability, allows for incremental development, and supports future expansion without significant refactoring.

### PRINCIPLE_3: **Data Integrity and Security**
- **RULE**: All data, especially sensitive content, MUST be handled with strict adherence to security best practices. Data storage and retrieval mechanisms MUST prioritize integrity, consistency, and access control. Secrets (API keys, credentials) MUST never be hardcoded or committed to version control; environment variables MUST be used.
- **RATIONALE**: Protects intellectual property, ensures reliability of information, and prevents unauthorized access or data corruption.

### PRINCIPLE_4: **Developer Experience and Tooling**
- **RULE**: The development environment MUST be consistent and well-documented. Required tooling MUST be integrated and utilized to streamline workflows and enforce coding standards.
- **RATIONALE**: Maximizes developer productivity, minimizes onboarding time, and reduces cognitive load by standardizing tools and processes.

### PRINCIPLE_5: **Observability and Reliability**
- **RULE**: All services and applications MUST incorporate comprehensive logging, metrics, and tracing. Error handling MUST be robust, with clear alerting mechanisms for critical issues.
- **RATIONALE**: Enables proactive monitoring, rapid debugging, performance analysis, and ensures system stability and uptime.

### PRINCIPLE_6: **Version Control and Immutability**
- **RULE**: All codebase changes MUST be managed through a robust version control system (Git). Core intellectual property, once published, SHOULD be treated as immutable, with new versions or amendments clearly delineated.
- **RATIONALE**: Ensures traceability of changes, facilitates collaboration, and maintains the integrity of published content.

### PRINCIPLE_7: **Open Standards and Interoperability**
- **RULE**: Where possible, open standards and well-established protocols MUST be favored for data formats, APIs, and communication. Proprietary solutions SHOULD be avoided unless critically necessary.
- **RATIONALE**: Promotes broad compatibility, reduces vendor lock-in, and encourages community contributions.

### PRINCIPLE_8: **User-Centric Design**
- **RULE**: All features and interfaces MUST be designed with the end-user in mind, prioritizing ease of use, accessibility, and a positive learning experience for students and researchers.
- **RATIONALE**: Ensures the product meets the needs of its audience, drives adoption, and maximizes educational impact.

### PRINCIPLE_9: **Continuous Improvement and Feedback**
- **RULE**: The project MUST embrace an iterative development approach. Mechanisms for collecting user feedback and incorporating it into future iterations MUST be established.
- **RATIONALE**: Fosters innovation, allows for rapid adaptation to user needs, and ensures the product remains relevant and high quality.

### PRINCIPLE_10: **Ethical AI Deployment**
- **RULE**: All AI components, especially the RAG chatbot, MUST be developed and deployed with strict adherence to ethical AI principles, including fairness, transparency, and accountability. Bias mitigation strategies MUST be actively pursued.
- **RATIONALE**: Builds trust with users, prevents harmful outcomes, and aligns with responsible AI development practices.

## 5. Development Guidelines

- **CODE_QUALITY**: Adhere to language-specific style guides (PEP 8 for Python, Airbnb for JavaScript/React). Automated formatting (Black, Prettier) and linting (MyPy) MUST be used.
- **TESTING**: Unit, integration, and end-to-end tests MUST be written for all critical components and features. Code coverage targets WILL be established and enforced.
- **DOCUMENTATION**: All significant architectural decisions MUST be documented as ADRs (`history/adr/`). All user interactions and development prompts MUST be captured as PHRs (`history/prompts/`). API endpoints MUST be documented with OpenAPI/Swagger.
- **VERSION_CONTROL**: Gitflow or similar branching strategy MUST be followed. Feature branches for all development, pull requests for code review, and clear commit messages.

## 6. Technology Choices Locked

- **BACKEND**: FastAPI (Python)
- **FRONTEND**: Docusaurus 3.9 (React/Markdown)
- **DATABASE**: Qdrant Cloud (Free Tier)
- **LLM_INTEGRATION**: Gemini API / OpenAI ChatKit
- **DEVELOPMENT_METHODOLOGY**: SpecKit Plus
- **AGENTIC_TOOLS**: Claude Code (CLI)

## 7. Constraints and Non-Goals

- **PERFORMANCE_TARGET**: Initial p95 latency for RAG queries <= 2 seconds. Will be refined post-MVP.
- **COST_BUDGET**: Adherence to Qdrant Cloud Free Tier and efficient LLM API usage. Cost-optimization strategies WILL be integrated.
- **NON_GOAL_COMPLEXITY**: Avoid premature optimization or over-engineering. Focus on delivering core functionality and user value before adding extensive features.
- **NON_GOAL_REAL_TIME_ROBOT_CONTROL**: Direct control or simulation of physical robots is outside the scope of this project.

## 8. Quality Standards (Non-Functional Requirements)

- **AVAILABILITY**: 99.9% uptime for core services.
- **SECURITY**: Regular security audits, dependency scanning, and adherence to OWASP Top 10. All external interfaces MUST be authenticated and authorized.
- **MAINTAINABILITY**: Code must be readable, well-structured, and easily extendable. Technical debt MUST be actively managed.
- **USABILITY**: Frontend interface must be intuitive and responsive across devices. Chatbot interactions must be natural and helpful.

## 9. Required Tooling

- Docusaurus (Frontend framework)
- FastAPI (Backend framework)
- Qdrant (Vector database)
- Gemini API / OpenAI ChatKit (LLM integration)
- Claude Code (AI Assistant CLI)
- SpecKit Plus (Spec-Driven Development framework)
- Git (Version Control)
- Docker (Containerization - planned for deployment)
- Python (Development language)
- Node.js / npm (Frontend tooling)

## 10. Requirements Regarding Reusable Intelligence (Agents, Subagents, Skills)

- **CLAUDE_CODE_UTILIZATION**: Claude Code (and any embedded agents/subagents) MUST be the primary interface for development tasks, code generation, refactoring, and documentation assistance.
- **AGENT_PROMPTS**: All agent prompts MUST be version-controlled and treated as first-class citizens in the codebase, residing in `.claude/agents/` or similar structured directories.
- **SKILL_DEVELOPMENT**: Custom skills SHOULD be developed to encapsulate repeatable, complex workflows specific to this project, enhancing agent efficiency.
- **EVALUATION**: Agent outputs and skill performance MUST be regularly evaluated for accuracy, efficiency, and adherence to project standards.

## 11. PHR/ADR Compliance Rules

- **PHR_MANDATORY**: A Prompt History Record (PHR) MUST be created for every significant user interaction, development step, and decision, documenting the prompt, response, and outcome. PHRs MUST be routed to `history/prompts/<feature-name>/` or `history/prompts/general/` as appropriate.
- **ADR_MANDATORY_SUGGESTION**: Architectural Decision Records (ADRs) MUST be suggested by the AI assistant for any decision meeting the criteria of significant impact, multiple alternatives, and cross-cutting scope. ADRs MUST be stored in `history/adr/`. The AI assistant MUST NOT auto-create ADRs without explicit user consent.
- **FORMAT_COMPLIANCE**: Both PHRs and ADRs MUST adhere strictly to their respective templates and maintain consistent formatting. All placeholders MUST be resolved.