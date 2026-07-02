# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-06-30

### Added
- **Core Optimization Engine (`ga_engine.py`)**: Implemented Genetic Algorithm with nonlinear learning rate growth, consecutive active skill fatigue penalization, constraints validation, and IELTS band score rounding (to nearest 0.25/0.75).
- **Multi-Agent Orchestrator (`agents.py`)**: Introduced `CoachAgent` (planner & tool caller) and `ReviewerAgent` (LLM-as-a-Judge) using the Agno framework. Supported adaptive model switching between local LiteLLM gateway and direct Google Gemini API (`gemini-2.5-flash`).
- **Interactive Command-Line (`cli.py`)**: Created terminal interface using Rich styling. Implemented interactive chat mode and direct parameter flags, with real-time logs streaming under the layout.
- **Web Interface (`app.py`)**: Designed dark-themed Streamlit interface. Features sidebar parameters sliders, Coach Chat box, weekly schedule card widgets, Matplotlib-rendered predicted learning curve lines, and trace logs viewer.
- **Model Context Protocol (`mcp_server.py`)**: Created FastMCP stdio server exposing GA scheduling tool.
- **Large-Scale Simulation (`simulation.py`)**: Added simulation script to evaluate performance on 100 randomized student profiles, achieving 72% overall success rate and saving metrics to `docs/simulation_results.png`.
- **Comprehensive Tests (`tests/`)**: Developed 16 tests covering GA math boundaries, Agno agents integration, and command parser.
- **Project Documentation**: Added `README.md`, `ARCHITECTURE.md`, and `docs/API.md`.
