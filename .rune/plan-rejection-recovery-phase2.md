# Phase 2: Workflow Integration & Rejection 1-Retry

This phase integrates the feasibility check and the single-retry rejection recovery logic into the orchestration flow.

## 1. Data Flow
```
[User Message] ──► [Parse Parameters via Regex]
                         │
        ┌────────────────┴────────────────┐
        ▼ (Plan Request)                  ▼ (Normal Chat)
[Feasibility Check]              [Invoke Coach Agent]
   │                                      │
   ├── (Infeasible) ──► Return Msg        ▼
   │ (Feasible)                    [Return Coach Advice]
   ▼
[Invoke Coach (GA)] ──► [Invoke Reviewer] ──► (Approved) ──► Return Plan
                               │
                               ▼ (Rejected L1)
                       [Retry Coach w/ Review Feedback]
                               │
                               ▼
                       [Invoke Reviewer L2] ──► (Approved) ──► Return Plan
                               │
                               ▼ (Rejected L2)
                       [Return HITL Verdict & Suggested Adjustments]
```

## 2. Code Contracts
In `ielts_coach/agents/coach.py`:
```python
_optimize_schedule_tool_called = False
def reset_tool_called() -> None: ...
def was_tool_called() -> bool: ...
```

In `ielts_coach/workflow.py`:
- Use regex patterns to extract current scores, target scores, and days from user message.
- Parse max hours from string (or default to 4.0).
- Wrap `execute_study_plan_flow(user_message)` to include retry loop and validation step.

## 3. Tasks
- **Task 2.1**: Implement `reset_tool_called()` and `was_tool_called()` in `ielts_coach/agents/coach.py` and set the flag `_optimize_schedule_tool_called = True` in `optimize_schedule_tool`.
- **Task 2.2**: Implement regex parsing in `ielts_coach/workflow.py` to extract L, R, W, S current/target scores and prep days. Support extracting "maximum of X hours per day" or default to 4.0.
- **Task 2.3**: Update `execute_study_plan_flow` in `ielts_coach/workflow.py` to call `check_feasibility` if a plan request is parsed. If infeasible, immediately return a structured failure response without running GA or LLM.
- **Task 2.4**: Implement the 1-retry recovery loop in `execute_study_plan_flow` if the first reviewer response starts with or contains "REJECTED".
- **Task 2.5**: Ensure `has_schedule` checks `was_tool_called()` rather than generic substring checks on the Coach's text response to prevent false reviews on general chat.

## 4. Failure Scenarios
| When | Then | Error / Response |
| :--- | :--- | :--- |
| First review rejected | Call Coach again with reviewer comments | Step: "warning", message: reviewer reason |
| Second review rejected | Stop, return approved=False + HITL instructions | Step: "failed", message: final rejection |
| Regex fails to parse scores in general chat | Proceed as normal chat, skip feasibility check | Safe fallback to standard conversational flow |

## 5. Rejection Criteria
- **DO NOT** execute more than 1 retry cycle to preserve token limits.
- **DO NOT** trigger the Reviewer Agent if the GA tool was not run.

## 6. Cross-Phase Context
- **Assumes**: `check_feasibility` function from Phase 1.
- **Exports**: Updated workflow execution API to Phase 3.

## 7. Acceptance Criteria
- Running workflow with general chat queries does NOT call the Reviewer Agent.
- Inputting infeasible scores immediately terminates and returns suggested adjustments.
- Rejecting a schedule triggers a secondary run which is logged in `logs/agent.log`.

<!-- outcome -->
### Outcome Block
- **What Was Planned**: Workflow orchestration update to support feasibility checks and 1-retry loops.
- **Immediate Next Action**: Modify `ielts_coach/agents/coach.py` and `ielts_coach/workflow.py`.
- **How to Measure**:
  | Test Case | Command / Action | Expected Result |
  | :--- | :--- | :--- |
  | Verify Workflow Logic | Mock tests or run python script | Check retry logs and feasibility block outputs |
