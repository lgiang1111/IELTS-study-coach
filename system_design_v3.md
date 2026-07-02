# IELTS Study Coach — Lean 2-Agent System Design (Agno Framework)

> AI Agent system for optimizing IELTS study schedules using Genetic Algorithms, built on the Agno Framework with Gemini models, utilizing a lean 2-agent architecture: Main Agent (Coach) and Reviewer Agent (Pedagogical Judge).

---

## 1. System Overview

### The Problem
Over 4 million IELTS test-takers each year must plan their study schedules across 4 skills (L/R/W/S) — a multi-dimensional optimization problem that humans cannot solve intuitively. Two primary issues:
1. **Suboptimal Time Allocation**: Students often focus too much on their weakest skill, ignoring the law of diminishing returns (*diminishing returns*).
2. **Ignoring Cognitive Fatigue**: Manual scheduling fails to model the non-linear relationship between continuous study duration and performance decline.

### The Solution
The **IELTS Study Coach** is a lean multi-agent system comprising **2 collaborative Agents**:
- **Main Agent (IELTS Study Coach)**: Handles user interaction, reasoning (ReAct), and calls computational tools (GA Optimizer, Score Predictor) to propose study schedules and provide strategic advice.
- **Reviewer Agent (Pedagogical Judge)**: Independently evaluates the schedule proposed by the Main Agent against pedagogical standards and practical constraints before displaying it to the user, ensuring quality and feasibility.
- **Genetic Algorithm Engine**: The mathematical optimization backend that resolves the workload distribution problem.

---

## 2. System Architecture

```
                        ┌────────────────────────┐
                        │     USER (Streamlit)   │
                        └───────────▲────────────┘
                                    │ Input / Output (Chat UI)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   MAIN AGENT: IELTS STUDY COACH (Agno)                 │
│                                                                        │
│   - Receives study requests or feedback from the User.                 │
│   - Uses ReAct loop to determine tool calls.                           │
│   - Invokes GA Optimizer Tool to generate or adjust study plans.       │
└───────────┬────────────────────────────────────────────▲───────────────┘
            │                                            │
            │ 1. Sends raw plan for review               │ 2. Returns evaluation
            ▼                                            │ (Approved / Issues)
┌────────────────────────────────────────────────────────┴───────────────┐
│                   REVIEWER AGENT: PLAN REVIEWER (Agno)                 │
│                                                                        │
│   - Receives study schedules from the Main Agent.                      │
│   - Acts as a Judge to evaluate pedagogical compliance criteria.        │
└────────────────────────────────────────────────────────────────────────┘
```

**Main Workflow execution logic:**
1. The **User** requests a study schedule via the Streamlit interface.
2. The **Main Agent** reasons and invokes the `generate_plan` tool (which runs the Genetic Algorithm) to produce a raw JSON schedule.
3. Before rendering the schedule to the user, the **Main Agent** automatically calls the **Reviewer Agent**, passing the raw JSON schedule and user context.
4. The **Reviewer Agent** analyzes the schedule. If it is APPROVED, the Main Agent formats it nicely and sends it to the user. If issues are found (REJECTED with specific recommendations), the Main Agent initiates a self-healing re-optimization loop or prompts the user with recommended adjustments.

---

## 3. Implemented AI Agent Concepts (5 Concepts)

The system implements **5 core Agent concepts** to fulfill evaluation standards:

| # | Concept | Application in the System |
|---|-----------|-----------------------------|
| 1 | **Multi-Agent Collaboration** | Decentralized responsibilities: The Main Agent handles user interaction and optimization; the Reviewer Agent validates pedagogical quality. |
| 2 | **Tool Use (Function Calling)** | The Main Agent calls Python tools to execute the Genetic Algorithm (`generate_plan`) and predict learning curves (`predict_score`). |
| 3 | **Reasoning & Planning (ReAct)** | The Main Agent reasons about user inputs -> decides which tool to call -> analyzes outputs -> sends them for review -> generates the final response. |
| 4 | **LLM-as-Judge (Evaluation)** | The Reviewer Agent acts as an independent evaluator, assessing study plans without self-bias from the Main Agent. |
| 5 | **Human-in-the-Loop** | Users provide feedback regarding cognitive fatigue or schedule changes -> The Main Agent automatically calls `adjust_plan` to re-optimize based on human input. |

---

## 4. 2-Agent Configuration Details (Agno Framework)

```python
from agno.agent import Agent
from agno.models.google import Gemini

# 1. REVIEWER AGENT: Acts as a pedagogical judge (LLM-as-Judge)
reviewer_agent = Agent(
    name="IELTS Plan Reviewer",
    role="Pedagogical expert evaluating and approving IELTS study schedules",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=[
        "Your task is to evaluate the IELTS study schedule generated by the Main Agent.",
        "Verify the following criteria carefully:",
        "  1. Are all 4 skills (Listening, Reading, Writing, Speaking) included in the 7-day cycle?",
        "  2. Is each study block at least 45 minutes and no more than 120 minutes?",
        "  3. Are there no more than 4 blocks per day to prevent cognitive overload?",
        "  4. Is the sequence logical (e.g., no consecutive intensive Writing blocks)?",
        "If the schedule meets all requirements, respond starting with 'APPROVED'.",
        "If errors or inconsistencies are found, respond with 'REJECTED' followed by a bulleted list of issues and suggested changes."
    ]
)

# 2. MAIN AGENT: Interactive Study Advisor for the User
main_agent = Agent(
    name="IELTS Study Coach",
    role="Personal assistant for scheduling and advising on optimal IELTS preparation pathways",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[generate_plan_tool, predict_score_tool, adjust_plan_tool],
    instructions=[
        "You are a professional IELTS Study Coach.",
        "1. Chat friendly and advise on study strategies matching the user's current and target bands.",
        "2. When the user requests a study plan, call the `generate_plan` tool.",
        "3. When the user reports fatigue or wants to adjust schedules, call the `adjust_plan` tool.",
        "4. MANDATORY: All newly created or adjusted schedules must be evaluated by the Reviewer Agent before display.",
        "   - If the Reviewer rejects the plan (REJECTED), re-run optimization with adjusted weights or explain the reasons and options to the user.",
        "   - If the Reviewer approves (APPROVED), format the schedule into a clean, markdown table with emojis.",
        "5. Respond in the same language as the user query (default is English)."
    ],
    show_members_responses=False # Orchestrate calls to the Reviewer Agent programmatically via Python code
)
```

---

## 5. Tools Specifications (Wrapped Python Functions)

The Main Agent uses 3 Python tools to interface with the core optimization engine:

### Tool #1: `generate_plan`
- **Purpose:** Runs the Genetic Algorithm to create an optimal 7-day schedule based on current and target scores.
- **Inputs:**
  - `initial_bands`: `dict` (L, R, W, S)
  - `target_band`: `float`
  - `total_days`: `int`
  - `hours_per_day`: `float`
- **Output:** JSON containing the 7-day study layout (`weekly_plan`), projected bands (`predicted_scores`), and cumulative fatigue indicator (`fatigue_score`).

### Tool #2: `predict_score`
- **Purpose:** Predicts IELTS band scores after a period of studying under the current plan (utilizing the learning curve model).
- **Inputs:**
  - `current_bands`: `dict` (L, R, W, S)
  - `plan_json`: `str` (JSON representation of the schedule)
  - `days`: `int`
- **Output:** JSON containing detailed band forecasts for all 4 skills and overall.

### Tool #3: `adjust_plan`
- **Purpose:** Re-runs GA optimization when receiving user fatigue feedback (Human-in-the-Loop).
- **Inputs:**
  - `current_plan_json`: `str`
  - `feedback`: `str` ("writing_too_tiring", "missed_day", "reduce_hours")
  - `adjustment_type`: `str` ("reduce_fatigue", "reschedule", "change_focus")
- **Output:** JSON containing the revised schedule after raising fatigue penalties in the GA fitness weights.

---

## 6. Execution Scenarios

### Scenario 1: Generating a New Study Plan
```
User: "My current scores are L: 6.0, R: 6.0, W: 5.0, S: 5.0. Target overall is 6.5 in 30 days, studying 3 hours daily."

Main Agent [Thought]: User wants a new study plan. I will invoke generate_plan.
Main Agent [Action]: Call generate_plan(initial={L:6.0, R:6.0, W:5.0, S:5.0}, target=6.5, days=30, hours=3)
GA Engine: Run Genetic Algorithm for 100 generations... Returns Plan JSON.

Main Agent [Thought]: Send this Plan JSON to Reviewer Agent for quality control.
Main Agent [Action]: Call Reviewer Agent (passes Plan JSON + user context).
Reviewer Agent [Thought & Action]: Evaluate plan. Checked 4 skills, block durations, no overload.
Reviewer Agent [Response]: "APPROVED: The schedule looks great and balances the workload across all skills."

Main Agent [Thought]: Plan is approved. I will format it nicely for the user.
Main Agent [Response]:
  "Based on your targets, I have designed an optimized study plan using a Genetic Algorithm. The schedule has been approved by the Reviewer Agent:
  
  📅 Day 1: Writing (60m) ➔ Reading (60m) ➔ Listening (45m)
  📅 Day 2: Speaking (45m) ➔ Writing (45m) ➔ Reading (45m)
  ...
  📊 Predicted Scores after 30 days: L: 6.5, R: 6.5, W: 6.0, S: 6.0 ➔ Overall: 6.5
  ⚡ Expected Fatigue Index: 35/100 (Safe)
  
  Would you like to make any adjustments?"
```

### Scenario 2: Fatigue Feedback (Human-in-the-Loop)
```
User: "Studying Writing for 60 minutes continuously on Day 1 is too tiring, I can't concentrate."

Main Agent [Thought]: User reports fatigue. Need to reduce Writing block duration. Call adjust_plan.
Main Agent [Action]: Call adjust_plan(current_plan, feedback="writing_too_tiring", type="reduce_fatigue")
GA Engine: Increase penalty weight for Writing fatigue, re-run GA... Returns new Plan with Writing reduced to 45m and interspersed breaks.

Main Agent [Thought]: Send new plan to Reviewer Agent for validation.
Main Agent [Action]: Call Reviewer Agent (passes new Plan).
Reviewer Agent [Response]: "APPROVED: Reducing Writing block duration improves cognitive retention."

Main Agent [Response]:
  "I have adjusted your schedule based on your feedback:
  ✅ Reduced continuous Writing blocks from 60 to 45 minutes.
  ✅ Interspersed breaks and rotated skills to avoid cognitive overload.
  
  📅 Day 1 (Revised): Reading (45m) ➔ Writing (45m) ➔ Speaking (45m)
  ...
  This updated schedule will help you study more sustainably!"
```

---

## 7. Mathematical Foundation (Core Engine)

The scheduling backend relies on mathematical models to ensure plan optimality:

### 7.1 Learning Curve Model
The improvement of individual skills follows an exponential saturation curve:

$$P_n = P_\infty - (P_\infty - P_0) \cdot e^{-kt}$$

- $P_n$: Predicted band score after $t$ hours.
- $P_\infty$: Theoretical ceiling band (9.0).
- $P_0$: Initial band score of the student.
- $k$: Learning rate coefficient (varies by skill: L/R are typically faster than W/S).
- $t$: Cumulative active study duration (hours).

### 7.2 Cognitive Fatigue Function
Models concentration depletion based on continuous session duration and mental variety rewards:

$$f(P) = \sum_{j=1}^{m} C_j \cdot t_j^\alpha - \beta \sum_{j=2}^{m} \mathbb{1}[s_j \neq s_{j-1}]$$

- $C_j$: Cognitive weight coefficient of skill $j$ (Writing/Speaking require active generation, hence higher $C_j$).
- $t_j$: Continuous session duration of block $j$ (hours).
- $\alpha$: Non-linear fatigue exponent (usually between $1.2$ and $1.5$).
- $\beta$: Variety reward coefficient for switching skills between consecutive sessions.
- $s_j$: Active skill of current block compared to the previous block.

### 7.3 Genetic Algorithm Fitness Function
GA searches for schedules that maximize predicted score progression while minimizing fatigue:

$$F(P) = \sum_{i=1}^{4} P_{n,i} - \text{NormalizedFatigue} \times \text{MaxPenaltyBandEquivalent}$$

---

## 8. Codebase Directory Layout

The directory structure separates Agent coordination (Agno) from core mathematical calculations:

```
ielts-study-coach/
├── README.md                 # Setup instructions, architecture overview, screenshots
├── requirements.txt          # Dependencies: agno, google-genai, streamlit, numpy, pyyaml
├── .env.example              # Example environment variable file
│
├── app.py                    # Streamlit Web UI (Chat interface & visualizations)
│
├── ielts_coach/              # Core Python package
│   ├── __init__.py
│   ├── ga_engine.py          # Core Genetic Algorithm (population=300, generations=100)
│   ├── workflow.py           # Sequential orchestration pipeline coordinating agents
│   └── agents/               # Multi-Agent sub-package
│       ├── __init__.py
│       ├── base.py           # Model factory, logging, and execution wrappers
│       ├── coach.py          # Coach Agent and skill tools
│       ├── reviewer.py       # Reviewer Agent (Pedagogical Judge)
│       └── security.py       # Security Guardrail Agent (Regex & LLM checks)
│
└── tests/                    # Pytest suites
    ├── test_agents.py        # Unit tests for individual agents
    ├── test_ga.py            # Unit tests for Genetic Algorithm engine
    └── test_integration.py   # Integration tests for agent workflow pipeline
```

---

## 9. Deliverables & Kaggle Evaluation Criteria

To meet all Kaggle competition criteria:
1. **GitHub Repository**: Organized modular structure, complete docstrings, and a comprehensive `README.md` with system architecture diagrams.
2. **Kaggle Writeup**: Detailed report explaining the problem, the lean 2-agent architecture, the integration of Genetic Algorithms, and simulation benchmarks.
3. **Demo Video (YouTube < 5m)**: Short video covering the problem statement ➔ Architecture ➔ Streamlit Web UI demo (schedule generation, security block, and feedback loop).
4. **Deployed Link**: Web app deployed on public clouds (e.g., Streamlit Community Cloud) allowing evaluators to interact with the system live.
