# Debug Knowledge Base

### 2026-07-01 — Streamlit Old Module Caching
- **Symptom**: Modified `workflow.py` did not execute its new retry logic in the Streamlit application interface, resulting in standard rejection logs without retries.
- **Root Cause**: The Streamlit server process was running continuously since 10:53 AM and cached the old module import in memory. Rerunning Streamlit UI only triggers re-execution of `app.py` but does not reload helper module scripts.
- **Fix**: Restarted the Streamlit server background process (`kill` PID and restart with `nohup streamlit run app.py`).
- **Files**: `ielts_coach/workflow.py`, `app.py`
