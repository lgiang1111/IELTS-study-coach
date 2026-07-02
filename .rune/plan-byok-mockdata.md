I will view the plan rules to follow the required format for implementation planning.

Viewed rune-plan.md:1-353

Here is the implementation plan for Option 1, including the User-provided API Key input and the Mock Scenario Simulator.

## Inline Plan: API Key Configuration & Mock Scenarios

### 1. Overview of Changes
We will modify the Streamlit UI, the CLI, and the workflow engine to support custom `GEMINI_API_KEY` inputs. If no API Key is provided, the UI will shift into **Demo Scenario Mode**, allowing the user to select and run high-fidelity simulations of all major agent execution paths (complete with step-by-step logs, timeline animations, and final plans).

### 2. Affected Files
1. **`ielts_coach/mock_data.py`** (New File): Houses static mock data, logs, and steps for the 5 key test cases.
2. **`ielts_coach/workflow.py`**: Add `mock_scenario` and `api_key` parameters to `execute_study_plan_flow()`. If `mock_scenario` is selected, it will stream mock logs and return the pre-defined scenario results.
3. **`app.py`**: Add Sidebar input for Gemini API Key. If empty, hide the direct optimization button and display the "Demo Scenario Mode" dropdown and trigger button instead.
4. **`cli.py`**: Support running mock scenarios or prompting for API keys.

---

### 3. Simulation Cases (`ielts_coach/mock_data.py`)
*   **Case 1: Successful Optimization** (`success`)
    *   *Path*: Guardrail OK → Feasibility OK → Coach GA Optimizes → Reviewer APPROVED.
*   **Case 2: Mathematically Infeasible Goal** (`infeasible`)
    *   *Path*: Guardrail OK → Feasibility Fails → System blocks immediately with suggestions.
*   **Case 3: Self-healing Rejection & Recovery** (`self_healing`)
    *   *Path*: Guardrail OK → Feasibility OK → Coach GA Optimizes → Reviewer REJECTED L1 → Coach Auto-retries → Reviewer APPROVED L2.
*   **Case 4: Double Rejection & HITL Fallback** (`double_rejection`)
    *   *Path*: Guardrail OK → Feasibility OK → Coach GA Optimizes → Reviewer REJECTED L1 → Coach Auto-retries → Reviewer REJECTED L2 → Escalate to Vietnamese suggestion box.
*   **Case 5: Safety Guardrail Blocked** (`guardrail_blocked`)
    *   *Path*: Guardrail Fails (Injection/Out-of-scope) → Blocks prompt immediately.

---

### 4. Code Design

#### `ielts_coach/mock_data.py`
```python
MOCK_SCENARIOS = {
    "success": {
        "steps": [...],
        "logs": [...],
        "output": "...",
        "approved": True
    },
    ...
}
```

#### `ielts_coach/workflow.py`
```python
def execute_study_plan_flow(user_message, api_key=None, mock_scenario=None, max_hours=None):
    if mock_scenario:
        # 1. Retrieve mock data
        # 2. Iterate through logs, logging them with a short sleep delay (e.g., 0.1s)
        #    to simulate live execution streaming
        # 3. Return mock steps, output, and status
        ...
```

#### `app.py`
```python
# Sidebar
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Enter your key from Google AI Studio")

if not api_key:
    st.sidebar.warning("⚠️ Vui lòng nhập API Key để tạo lịch học tùy chỉnh.")
    st.sidebar.info("💡 Bạn có thể chọn các kịch bản Demo dưới đây để trải nghiệm tính năng mà không cần API Key:")
    demo_scenario = st.sidebar.selectbox("Chọn kịch bản Demo", [
        ("Thành công - Tối ưu và Duyệt", "success"),
        ("Mục tiêu bất khả thi - Bị chặn", "infeasible"),
        ("Tự sửa đổi - Reviewer từ chối lần 1 & Duyệt lần 2", "self_healing"),
        ("Thất bại - Từ chối 2 lần & Gợi ý HITL", "double_rejection"),
        ("Vi phạm Guardrail - Bị chặn an toàn", "guardrail_blocked")
    ], format_func=lambda x: x[0])
    
    if st.button("🚀 Chạy Kịch bản Demo"):
        # Run flow with mock_scenario=demo_scenario[1]
        ...
else:
    # Render original prompt parameters input & "Optimize Schedule" button
    ...
```

---

### 5. Non-Functional Requirements & Rejections
*   **DO NOT** expose API keys in frontend inputs or URL params.
*   **DO NOT** execute any live Gemini API calls if `api_key` is empty or if running in `mock_scenario` mode.
*   **DO** preserve all log styling, terminal outputs, and the sidebar timeline execution visual steps.

***

### Outcome Block

| What Was Planned | Immediate Next Action | How to Measure |
| :--- | :--- | :--- |
| Implement API Key configuration block & Mock Scenario simulation engine. | Create `ielts_coach/mock_data.py` and populate it with high-fidelity mock data scenarios. | `pytest tests/` (ensuring existing tests pass). |

*Please confirm if you agree with the plan to begin implementation.*