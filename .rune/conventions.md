# Project Conventions: IELTS Study Coach Capstone

## 1. Naming Conventions
- **Files**: Use `snake_case.py` for Python source files and module files. Use `kebab-case.md` for documents and agent rules.
- **Functions & Variables**: Use `snake_case` in Python (e.g., `run_ga()`, `predict_score()`).
- **Classes**: Use `PascalCase` (e.g., `GeneticOptimizer`).
- **Constants**: Use `UPPER_CASE` (e.g., `MAX_PENALTY_BAND_EQUIVALENT`).

## 2. Import Style
- Group imports into:
  1. Standard library imports
  2. Third-party imports (numpy, agno, etc.)
  3. Local imports (engine, tools)
- Avoid wildcard imports (`from module import *`). Use explicit named imports.

## 3. Error Handling Pattern
- Wrap all optimization tools inside `try/catch` blocks.
- Return descriptive error messages as strings (for LLM context) instead of raising raw exceptions.
- Validate input variables (such as band score range `[0.0, 9.0]`) at the API entry point.

## 4. State Management
- Session state will be handled natively by Streamlit (`st.session_state`) for conversation history and current schedules.
- Agent routing states are kept stateless between turns, utilizing App Router to handle logic execution.

## 5. API Pattern
- Tools will be exposed using a custom Model Context Protocol (MCP) server or standard Agno `@tool` functions.
- All tools must return a stringified JSON format for the calling LLM to read.

## 6. Test Structure
- Unit tests for the Genetic Algorithm core (GA) and the mathematical formulas should be co-located or put under a `/tests` folder using `pytest`.

## 7. Model Versioning
- Avoid using legacy Google model IDs (e.g. `gemini-2.0-flash`). Use `gemini-2.5-flash` to ensure long-term compatibility with the Google GenAI SDK in Agno.

## 8. Client Key Instantiation
- Pass the `api_key` parameter directly into `Gemini(..., api_key=...)` in Agno instead of relying solely on environment variables to guarantee standalone runtime execution.

## 9. Reliable LLM Execution
- **Pattern**: Wrap all LLM/Agent calls in a resilient retry helper with exponential backoff (`run_agent_with_retry`) to handle temporary 503/429 errors from the model provider. Use `is_json_error` to catch raw provider errors and format them into clean Markdown warnings.
- **Example**: `coach_content = run_agent_with_retry(coach, user_message)`
- **Applies to**: Any module directly calling an agent or LLM (e.g. `ielts_coach/agents/base.py`).

## 10. 100% English UI & Code Base
- **Pattern**: All UI widgets, logs, system errors, mock scenarios, test assertions, and user-facing notifications must be written in English. Do not mix English and Vietnamese.
- **Applies to**: Streamlit UI (`app.py`), orchestrator (`workflow.py`), agents, tests, and CLI outputs.

## 11. LAN Deployment Binding
- **Pattern**: Bind local test servers to all interfaces (`0.0.0.0`) instead of `127.0.0.1` when local area network sharing or cross-device visual checking is desired.
- **Applies to**: Streamlit run commands or other microservice endpoints.

## 12. Styled Log Presentation
- **Pattern**: Render agent and system tracing logs inside a scrollable `<div>` element instead of a `<pre>` element. Color-code components (e.g. `[INFO]`, `[Flow]`, `[Security]`) using inline span styling, and replace newlines `\n` with HTML `<br/>` tags to prevent Markdown parsing collapse of carriage returns. Show the newest log lines first at the top.



