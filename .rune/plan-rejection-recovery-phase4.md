# Phase 4: Integration Testing & UI Verification

This phase focuses on validating the entire multi-agent flow, checking integration correctness, and testing the system end-to-end.

## 1. Data Flow
```
[Test Script / Pytest] ──► [execute_study_plan_flow()] ──► [Assert response fields & step statuses]
```

## 2. Code Contracts
None. Uses test suite validation against existing orchestration code.

## 3. Tasks
- **Task 4.1**: Create `tests/test_integration.py` validating:
  - **Infeasible Pre-check**: Verify that calling the flow with an impossible score specification immediately returns a warning response, skips Coach Agent and Reviewer steps, and does not update `last_ga_result.json`.
  - **General Question Handling**: Verify that asking general questions (e.g. format, resources) does not invoke the Reviewer Agent and records appropriate steps.
  - **Rejection Recovery Logic**: Mock the Reviewer Agent to return "REJECTED" on first check and "APPROVED" on second check. Verify that the flow executes exactly 2 runs of the Coach Agent and finishes as approved.
- **Task 4.2**: Run the entire Pytest test suite to ensure all unit and integration tests pass successfully.

## 4. Failure Scenarios
| When | Then | Error / Response |
| :--- | :--- | :--- |
| Test suite fails | Trace error, fix implementation, and rerun tests | Non-zero exit code |

## 5. Rejection Criteria
- **DO NOT** commit untested flow logic.
- **DO NOT** mock the whole workflow in the integration test; verify the actual models/tools or use mock assertions specifically for LiteLLM calls where external endpoints are unstable.

## 6. Cross-Phase Context
- **Assumes**: Feasibility check, workflow updates, and UI updates are completed.
- **Exports**: Verified codebase ready for final documentation completion in Phase 5.

## 7. Acceptance Criteria
- Integration test suite passes.
- Overall pytest coverage includes the new files.

<!-- outcome -->
### Outcome Block
- **What Was Planned**: Integration test suite development and pipeline verification.
- **Immediate Next Action**: Implement `tests/test_integration.py` and run tests.
- **How to Measure**:
  | Test Case | Command / Action | Expected Result |
  | :--- | :--- | :--- |
  | Full Pytest Suite | `PYTHONPATH=. pytest` | All unit & integration tests pass |
