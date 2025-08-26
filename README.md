
# TalentScout — AI/ML Hiring Assistant
TalentScout is an LLM-powered chatbot for initial screening of technology candidates. It collects essential candidate details and generates tailored technical questions based on the declared tech stack, while maintaining conversational context, handling fallbacks, and concluding gracefully.

Features
Professional greeting, clear purpose, and conversation-ending keyword handling (quit, exit, stop, end, goodbye).

Guided intake: full name, email, phone, years of experience, desired positions, current location, tech stack.

Tech-stack-based question generation (3–5 per technology) using a curated YAML bank with LLM-ready hooks.

Context handling via session state and a clean Streamlit chat UI (one question at a time).

Fallback prompts, lightweight validation (email, phone, numeric experience), and secure environment-based configuration.

Architecture
Frontend: Streamlit chat interface (st.chat_message + st.chat_input).

Conversation management: Finite-state progression (greet → intake → assessment → summary → end), per-field validation, and clarification prompts.

Question generation: YAML-backed question bank (Python, JS, React, Node.js, Django, PostgreSQL, AWS, Docker), with a modular generator ready to swap in LLM calls.

Configuration & security: Environment variables via dotenv; .gitignore to exclude secrets, logs, and data.

Repository Structure
app.py — Streamlit app; conversation flow, validation, summary, and chat UI.

prompt_templates.py — System prompt, question-generation prompt, validation prompt, summary prompt.

question_generator.py — YAML-backed generator with per-tech sampling.

question_bank.yaml — Curated screening questions for common technologies.

data_handler.py — Pydantic model and end keywords for safe parsing.

config.py — Environment configuration (API keys, model name, project name).

requirements.txt — Project dependencies.

.env.example — Example environment variables (no secrets).

.gitignore — Excludes virtual env, .env, logs, data, caches, IDE files.

docs/architecture.png — Optional system diagram.

docs/flow.png — Optional conversation flow diagram.

tests/test_basic.py — Placeholder for basic tests.

Installation
Create and activate a virtual environment:

macOS/Linux: python -m venv .venv && source .venv/bin/activate

Windows (PowerShell): python -m venv .venv; ..venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Configure environment:

cp .env.example .env

Add your API key only if enabling live LLM generation (defaults use YAML bank).

Run the app:

streamlit run app.py

Usage
Follow the chatbot prompts to enter personal details and tech stack (comma-separated).

The assistant asks 3–5 short screening questions per technology and records answers.

Use quit/exit/stop/end/goodbye to end at any time.

The assistant provides a short recruiter-ready summary and next steps at the end.

Prompt Design
System prompt: Defines TalentScout’s role, tone, boundaries, and exit keywords.

Question generation: Requests practical, scenario-centric screening questions per technology with structured JSON output (ready to parse).

Validation prompt (optional): Asks the model to validate and normalize inputs with a strict JSON schema (local validators are included by default).

Summary prompt: Produces concise, recruiter-facing bullet points.

Conversation Flow
Stages: greet → name → email → phone → experience → positions → location → tech_stack → questions → summary → end.

One question at a time; unclear inputs trigger concise clarifications.

Question delivery iterates through technologies and their question lists with per-tech rotation.

Data Handling & Privacy
No real PII is stored in the repository; use only synthetic or anonymized data for demos.

Secrets (API keys) are loaded via environment variables; never commit secrets.

For public repositories, rely on secret scanning/push protection and manual review before pushing.

When deploying a demo, use platform secrets or environment variables and avoid sensitive content.

Security Practices
.gitignore excludes .env, logs, data dumps, caches, and editor metadata.

Environment-based secrets (OPENAI_API_KEY) and model selection via MODEL_NAME.

No hardcoded credentials; rotate keys promptly if accidentally exposed.

Optional Enhancements
Sentiment analysis for candidate tone and confidence indicators in summaries.

Multilingual support (auto-detect language and switch prompts/UX).

Advanced UI: progress stepper, restart action, export of candidate profile (JSON/CSV).

Cloud deployment (Streamlit Cloud, AWS/GCP/Azure) with restricted access for real data.

Testing
Unit tests for validation utilities and conversation state transitions.

Snapshot tests for prompt templates and JSON structures.

Linting/formatting with ruff/black (optional) and type checks with mypy/pyright (optional).

How to Push to GitHub (quick)
git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/USER/REPO.git

git push -u origin main

Ensure .env and any sensitive artifacts are excluded before pushing. If a secret was committed, rotate it and rewrite history if necessary.

License
This project is released under the MIT License. See LICENSE for details.

Acknowledgments
Streamlit chat patterns for conversational apps.

Common screening topics across Python/JS/React/Node/Django/PostgreSQL/AWS/Docker ecosystems.

Community best practices for environment-based configuration and secret hygiene.
