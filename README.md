# AI-Powered IELTS Study Coach Agent

An intelligent multi-agent system that generates personalized IELTS study schedules optimized via Genetic Algorithms (GA) while modeling cognitive fatigue and nonlinear learning rates.

> **Kaggle AI Agents Capstone** · Track: Agents for Good — Education  
> Key concepts: Multi-Agent (Agno) · MCP Server · Dual-Layer Security · Deployability · Agent Skills

---

## 🚀 Quick Start

### 1. Install Dependencies
Requires Python 3.10+. In the project root:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and set: GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the Application
*   **Web UI (Streamlit)**:
    ```bash
    PYTHONPATH=. streamlit run app.py
    ```
*   **CLI Interface (Rich)**:
    ```bash
    PYTHONPATH=. python3 cli.py
    ```
*   **MCP Server (stdio)**:
    ```bash
    PYTHONPATH=. python -m ielts_coach.mcp_server
    ```

> **No API key?** Both interfaces include a **Demo Mode** with 5 pre-built mock scenarios that showcase the full multi-agent pipeline without requiring any API credentials.

---

## ✨ Features

### Multi-Agent Pipeline
- **Security Guardrail Agent** (`agents/security.py`) — Dual-layer input filter: fast regex pattern matching + LLM semantic relevance check
- **Coach Agent** (`agents/coach.py`) — Planner that invokes the GA optimizer tool and SearXNG web search tool
- **Reviewer Agent** (`agents/reviewer.py`) — Independent pedagogical LLM-as-a-Judge critic
- **Workflow Coordinator** (`workflow.py`) — Deterministic sequential pipeline with structured step metadata

### Optimization Engine
- **Genetic Algorithm** (`ga_engine.py`) — Custom multi-objective optimizer with nonlinear learning curves, cognitive fatigue modeling, and IELTS band rounding
- **Feasibility Pre-Check** (`feasibility.py`) — Mathematical validation via inverted learning curves before any LLM/GA invocation, saving API costs
- **Rejection Recovery** — Automatic 1-retry self-healing loop on Reviewer rejection; escalates to Human-in-the-Loop parameter suggestions on persistent failure

### Deployability
- **Streamlit Web UI** — Dark-themed premium interface with gradient styling, sidebar score sliders, Agent Execution Timeline badges, Matplotlib learning curve charts, and color-coded trace log viewer
- **Rich CLI** — Beautiful terminal interface with interactive chat mode and parameter flags
- **MCP Server** — FastMCP stdio transport exposing the GA optimizer for external agent integration
- **Demo Mode** — 5 mock scenarios (Success, Infeasible, Self-Healing, Double Rejection, Security Block) for API-free demonstrations

### Security
- Layer 1: Compiled regex filter for prompt injection keywords (`ignore previous instructions`, `jailbreak`, `dan mode`, etc.)
- Layer 2: Dedicated `SecurityGuardrailAgent` for semantic relevance classification
- PII/key sanitization — environment variables never appear in log outputs

---

## 🛠 Tech Stack

| Layer | Technology |
|:---|:---|
| Agent Framework | [Agno](https://github.com/agno-agi/agno) (v2.6+) |
| LLM | Google Gemini 2.5 Flash via `google-genai` |
| Optimization | Custom Genetic Algorithm (pure Python + NumPy) |
| Web Search | Self-hosted SearXNG |
| MCP | FastMCP (python `mcp` v1.28+) |
| Web UI | Streamlit (v1.35+) |
| CLI | Rich (v13.7+) |
| Charts | Matplotlib + NumPy |
| Testing | pytest (v9.1+) |

---

## 📂 Project Structure

```
ielts-study-coach/
├── ielts_coach/                # Core Python package
│   ├── __init__.py
│   ├── ga_engine.py            # Genetic Algorithm: learning curves, fatigue, fitness
│   ├── feasibility.py          # Mathematical feasibility pre-checker
│   ├── workflow.py             # Sequential pipeline coordinator (5-stage flow)
│   ├── mcp_server.py           # FastMCP stdio server exposing GA tool
│   ├── mock_data.py            # 5 demo scenario datasets
│   └── agents/                 # Multi-Agent sub-package
│       ├── __init__.py
│       ├── base.py             # Model factory + resilient retry wrapper
│       ├── coach.py            # Coach Agent (GA optimizer + SearXNG tools)
│       ├── reviewer.py         # Reviewer Agent (Pedagogical Judge)
│       └── security.py         # Security Guardrail (Regex + LLM filters)
├── app.py                      # Streamlit web application (494 LOC)
├── cli.py                      # Rich CLI interface (258 LOC)
├── simulation.py               # 100-user quantitative simulation runner
├── requirements.txt            # Dependencies manifest
├── tests/                      # Automated test suite (24 tests)
│   ├── test_ga.py              # GA math unit tests (7)
│   ├── test_feasibility.py     # Feasibility checker tests (5)
│   ├── test_agents.py          # Agent construction tests (4)
│   ├── test_cli.py             # CLI parser tests (5)
│   └── test_integration.py     # End-to-end workflow tests (3)
├── KAGGLE_SUBMISSION.md        # Kaggle Capstone writeup
├── ARCHITECTURE.md             # System architecture documentation
├── CHANGELOG.md                # Version changelog
└── docs/                       # Supplementary documentation
    ├── API.md                  # API reference
    └── simulation_results.png  # 100-user simulation charts
```

**Total**: ~2,641 lines of Python across 14 source files + 5 test files.

---

## ⚙️ Configuration

Environment variables (`.env`):

| Variable | Required | Description |
|:---|:---|:---|
| `GEMINI_API_KEY` | Yes* | Google AI Studio API key for Gemini 2.5 Flash |
| `LITELLM_BASE_URL` | No | LiteLLM proxy URL (overrides direct Gemini) |
| `LITELLM_API_KEY` | No | API key for LiteLLM gateway |
| `SEARXNG_URL` | No | Self-hosted SearXNG search URL (default: `http://172.20.0.26:8888`) |

*Not required for Demo Mode.

---

## 🧪 Testing

Run the full test suite (24 tests):
```bash
PYTHONPATH=. pytest tests/
```

All tests pass on Python 3.12 with pytest 9.1.

---

## 📊 Simulation Results

100 randomized student profiles evaluated:
- **Target Success Rate**: 72.00%
- **Average Band Improvement**: +1.04 bands
- **Average Fitness Score**: 27.41

---

## 📄 License

This project was built for the [Kaggle AI Agents Intensive Vibe Coding Capstone](https://www.kaggle.com/competitions/ai-agents-intensive-vibe-coding-capstone-project) (June 2026).
