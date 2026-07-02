# Master Plan: Rejection Recovery & Feasibility Check

This master plan structures the implementation of the early feasibility checker and the 1-retry rejection recovery loop.

## Phase Overview

| Phase | Goal | Status | Touch Files |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Feasibility Checker Engine & Unit Tests | ✅ Completed | `ielts_coach/feasibility.py`, `tests/test_feasibility.py` |
| **Phase 2** | Workflow Integration & Rejection 1-Retry | ✅ Completed | `ielts_coach/workflow.py`, `ielts_coach/agents/coach.py` |
| **Phase 3** | App & CLI parameter updates (Max Daily Hours) | ✅ Completed | `app.py`, `cli.py` |
| **Phase 4** | Integration Testing & UI Verification | ✅ Completed | `tests/test_integration.py` |
| **Phase 5** | Documentation Completion & Submission Prep | ✅ Completed | `KAGGLE_SUBMISSION.md`, `README.md`, `ARCHITECTURE.md` |

## Key Decisions
- **Rule-based Pre-check**: Compute feasibility mathematically before calling GA or LLM to optimize speed and API costs.
- **Explicit GA Tool Call Detection**: Use a thread-safe flag to monitor actual tool execution, preventing false positive reviews on general chat inputs.
- **Retry Constraints**: Exactly one retry with appended reviewer comments, falling back to HITL on the second rejection.

## Dependencies & Risks
- **Risk**: Stochastic GA optimization might return the same plan on retry.
- **Mitigation**: Appending reviewer comments to the Coach prompt forces the Coach LLM to request parameter shifts or adjust advice in the final schedule.

<!-- outcome -->
### Outcome Block
- **What Was Planned**: Rejection recovery, feasibility validation, and Kaggle submission documentation.
- **Immediate Next Action**: Await user approval of the revised Master Plan.
- **How to Measure**:
  | Test Case | Command / Action | Expected Result |
  | :--- | :--- | :--- |
  | Master Plan Approval | User input approval | Prompt moves to phase file generation |
