---
id: 002
title: Generate project task breakdown
stage: tasks
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-book-core
branch: 001-book-structure
user: user
command: /sp.tasks
labels: ["project", "tasks"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- history/prompts/general/002-generate-project-task-breakdown.tasks.prompt.md
tests:

---

## Prompt

/sp.tasks

Generate the complete task breakdown for this project based strictly on the approved plan and spec.md.

For each milestone, produce:
- Task ID
- Task title
- Description
- Required files/directories
- Dependencies
- Acceptance criteria

Do NOT modify the spec.
Do NOT add new requirements.
Just convert the plan into actionable tasks.

## Response snapshot

Creating PHR for task breakdown generation.

## Outcome

- ✅ Impact: null
- 🧪 Tests: null
- 📁 Files: null
- 🔁 Next prompts: Generate task breakdown
- 🧠 Reflection: null

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
