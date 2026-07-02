# IELTS Study Coach Capstone — Project Configuration

## Overview
Capstone project researching and developing an AI Agent system integrated with a Genetic Algorithm to optimize IELTS study schedules and minimize student cognitive fatigue.

## Tech Stack
- Framework: Streamlit, Agno (formerly Phidata)
- Language: Python
- Package Manager: pip (via requirements.txt)
- Test Framework: pytest
- Build Tool: none
- Linter: none
- Python Environment: venv (.venv/)

## Directory Structure
- `.agent/rules/` - Rune rules and guidelines for agent behavior
- `.rune/` - AI session state, project conventions, and progress logs
- `docs/` - Advanced architecture, API specs, and Agno frameworks
- `logs/` - Logs directory storing execution trace and final schedules
- `tests/` - Pytest test files for GA engine, CLI, and Agents
- `ielts_coach/` - Core Python package:
  - `ga_engine.py` - Core Genetic Algorithm engine & cognitive fatigue calculations
  - `mcp_server.py` - Model Context Protocol stdio server exposing GA tool
  - `workflow.py` - Sequential pipeline coordinating the multi-agent workflow
  - `agents/` - Multi-Agent sub-package:
    - `base.py` - Shared runtime (logger, model factory, run retry wrapper)
    - `coach.py` - Coach Agent & skills (GA & SearXNG search tools)
    - `reviewer.py` - Reviewer Agent (Pedagogical Judge)
    - `security.py` - Security Guardrail Agent (Rule-based & LLM safety filters)
- `app.py` - Web-based interactive Streamlit user interface
- `cli.py` - Console-based Rich CLI interface
- `simulation.py` - Quantitative run simulations (100 users)

## Conventions
- Naming: snake_case for Python files/functions/variables, kebab-case for rules and docs
- Error handling: try-except wrappers returning stringified JSON messages
- State management: Streamlit session state & file-based persistence (logs/last_ga_result.json)
- API pattern: Model Context Protocol (MCP) and Agno tool definitions
- Test structure: Pytest test cases located in tests/

## Commands
- Install: pip install -r requirements.txt
- Dev: streamlit run app.py
- Build: none
- Test: PYTHONPATH=. .venv/bin/pytest tests/
- Lint: none

## Key Files
- Entry point: app.py (Web UI) & cli.py (CLI tool)
- Config: requirements.txt (Dependencies) & .env (Environment variables)
- Routes/API: ielts_coach/mcp_server.py (MCP Integration) & ielts_coach/workflow.py (Multi-Agent Flow)
