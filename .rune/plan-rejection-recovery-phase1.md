# Phase 1: Feasibility Checker Engine & Unit Tests

This phase builds the standalone mathematical feasibility checker module and its unit tests.

## 1. Data Flow
```
[User Input Scores & prep parameters] 
       │
       ▼
[check_feasibility()] ──► [Invert learning curve: t = (1/k) * ln((9-P0)/(9-Pn))]
       │
       ▼
[Feasibility Verdict & Suggestions]
```

## 2. Code Contracts
In `ielts_coach/feasibility.py`:
```python
def check_feasibility(
    initial_bands: dict[str, float], 
    target_bands: dict[str, float], 
    total_days: int, 
    max_daily_hours: float
) -> dict:
    """
    Returns:
    {
        "feasible": bool,
        "required_hours": float,
        "available_hours": float,
        "details": dict[str, float],
        "suggested_days": int (optional),
        "suggested_daily_hours": float (optional)
    }
    """
```

## 3. Tasks
- **Task 1.1**: Create `ielts_coach/feasibility.py` implementing `check_feasibility()` using the mathematical logic:
  - $t_s = \frac{1}{k_s} \ln\left(\frac{9.0 - P_{initial,s}}{9.0 - P_{target,s}}\right)$ for $P_{target,s} > P_{initial,s}$ (else $0$).
  - Cap target score $P_{target,s}$ at $8.9$ to avoid division by zero or negative logs.
  - $T_{avail} = \min(48.0, 7.0 \times H_{max\_daily}) \times \frac{\text{total\_days}}{7.0}$
  - Compare $T_{req} = \sum t_s$ vs $T_{avail}$.
- **Task 1.2**: Create `tests/test_feasibility.py` containing Pytest tests:
  - Test achievable plan (e.g. increase 0.5 band in 30 days with 4h/day).
  - Test impossible plan (e.g. increase 2.5 bands in 10 days with 1h/day).
  - Test edge cases: target equal to initial, target capped at 9.0.

## 4. Failure Scenarios
| When | Then | Error / Response |
| :--- | :--- | :--- |
| Target score >= 9.0 | Clip target to 8.9 in formula | Avoid Division by zero |
| Target score <= Initial | Set required hours to 0.0 | Graceful handling |
| Negative/zero days | Raise ValueError | Input validation safety |

## 5. Rejection Criteria
- **DO NOT** use LLM calls, embeddings, or agent reasoning inside `feasibility.py`. It must be 100% deterministic python code.
- **DO NOT** raise unhandled exceptions; return a safe result dictionary.

## 6. Cross-Phase Context
- **Assumes**: Math learning rates from `ga_engine.py`.
- **Exports**: `check_feasibility` helper to `ielts_coach/workflow.py` for Phase 2.

## 7. Acceptance Criteria
- Pytest suite `tests/test_feasibility.py` runs and passes with 100% success rate.
- Feasibility check is mathematically consistent with the GA learning curve limits.

<!-- outcome -->
### Outcome Block
- **What Was Planned**: Phase 1 feasibility check core library and tests.
- **Immediate Next Action**: Implement `ielts_coach/feasibility.py` and `tests/test_feasibility.py`.
- **How to Measure**:
  | Test Case | Command / Action | Expected Result |
  | :--- | :--- | :--- |
  | Feasibility Unit Tests | `PYTHONPATH=. pytest tests/test_feasibility.py` | All tests pass |
