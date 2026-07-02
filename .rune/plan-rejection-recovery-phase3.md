# Phase 3: App & CLI Parameter Updates (Max Daily Hours)

This phase updates the Streamlit UI and CLI interfaces to support max daily hours settings and display HITL recommendations.

## 1. Data Flow
```
[User UI/CLI Inputs] ──► [Construct Prompt w/ Max Hours] ──► [execute_study_plan_flow()]
                                                                      │
[Render HITL message / suggestions] ◄── [approved=False or Feasibility Fail] ┘
```

## 2. Code Contracts
None. Updates to standard entry point arguments and UI states.

## 3. Tasks
- **Task 3.1**: In `app.py` (Streamlit sidebar), add:
  ```python
  max_hours = st.slider("Max Daily Hours", 1.0, 8.0, 4.0, 0.5)
  ```
- **Task 3.2**: In `app.py` and `cli.py`, update prompt formatting:
  ```python
  prompt = (
      f"My current IELTS scores are L:{l_init}, R:{r_init}, W:{w_init}, S:{s_init}. "
      f"My target scores are L:{l_targ}, R:{r_targ}, W:{w_targ}, S:{s_targ}. "
      f"I want to optimize a {days}-day study plan. "
      f"I can study a maximum of {max_hours} hours per day."
  )
  ```
- **Task 3.3**: Update `app.py` display logic for rejected plans or feasibility failures. If a response is marked as infeasible or rejected:
  - Display a clean warning block (orange/red card).
  - List HITL suggestions: "Reduce target scores by 0.5 band", "Increase study days", or "Increase max daily study hours".
- **Task 3.4**: In `cli.py`, add the `--max-hours` CLI argument to `main()` (default: 4.0). Update the console trace formatting to output HITL alerts on rejection.

## 4. Failure Scenarios
| When | Then | Error / Response |
| :--- | :--- | :--- |
| Feasibility fails immediately | Display suggestions box on Streamlit UI immediately | No GA is run, UI displays warning |

## 5. Rejection Criteria
- **DO NOT** hardcode maximum hours; allow the user to control it from the UI.
- **DO NOT** use default plain colors for warnings; use beautiful custom CSS alerts matching the glassmorphism theme of the app.

## 6. Cross-Phase Context
- **Assumes**: Updated `execute_study_plan_flow` interface from Phase 2.
- **Exports**: Fully functional frontend and backend integration.

## 7. Acceptance Criteria
- Slider exists in the sidebar and updates the prompt correctly.
- If an infeasible setup is requested, a card immediately appears offering corrective recommendations.
- CLI handles `--max-hours` flag correctly.

<!-- outcome -->
### Outcome Block
- **What Was Planned**: UI and CLI integrations of the feasibility checker and max daily hours constraints.
- **Immediate Next Action**: Modify `app.py` and `cli.py`.
- **How to Measure**:
  | Test Case | Command / Action | Expected Result |
  | :--- | :--- | :--- |
  | Run Streamlit UI | `streamlit run app.py` | Verify sidebar slider and feasibility feedback cards |
