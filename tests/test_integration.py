# tests/test_integration.py
import pytest
from unittest.mock import patch, MagicMock
from ielts_coach.workflow import execute_study_plan_flow

def test_integration_feasibility_blocked():
    # Feasibility pre-check fails immediately
    prompt = (
        "My current IELTS scores are L:5.0, R:5.0, W:5.0, S:5.0. "
        "My target scores are L:8.5, R:8.5, W:8.5, S:8.5. "
        "I want to optimize a 10-day study plan. "
        "I can study a maximum of 2.0 hours per day."
    )
    
    result = execute_study_plan_flow(prompt)
    
    assert result["approved"] is False
    assert "Infeasible Study Target" in result["coach_response"]
    assert "Feasibility Warning" in result["coach_response"]
    
    # Check that the steps show failed for feasibility and skipped for Coach/Reviewer
    steps = result["steps"]
    assert steps[1]["name"] == "Feasibility Pre-Check"
    assert steps[1]["status"] == "failed"
    assert steps[2]["status"] == "skipped"

@patch("ielts_coach.workflow.validate_user_prompt")
@patch("ielts_coach.workflow.run_agent_with_retry")
@patch("ielts_coach.workflow.was_tool_called")
def test_integration_rejection_recovery_approved_on_retry(mock_was_tool_called, mock_run_agent, mock_validate):
    # Mock security check to pass
    mock_validate.return_value = (True, "")
    
    # Mock was_tool_called to return True
    mock_was_tool_called.return_value = True
    
    # Mock agent calls:
    # First call: Coach returns a plan
    # Second call: Reviewer returns REJECTED
    # Third call: Coach returns revised plan (on retry)
    # Fourth call: Reviewer returns APPROVED
    mock_run_agent.side_effect = [
        "Here is the proposed schedule...",  # Coach L1
        "REJECTED: Please add more speaking practice",  # Reviewer L1
        "Here is the revised schedule with more speaking...",  # Coach L2
        "APPROVED: Looks perfect!"  # Reviewer L2
    ]
    
    # Study duration: 30 days. Max daily hours: 6.0 -> Available = min(48, 42) * 30/7 = 180h > 142.6h (Feasible)
    prompt = (
        "My current IELTS scores are L:6.5, R:6.5, W:6.0, S:6.5. "
        "My target scores are L:7.0, R:7.0, W:6.5, S:6.5. "
        "I want to optimize a 30-day study plan. "
        "I can study a maximum of 6.0 hours per day."
    )
    
    result = execute_study_plan_flow(prompt)
    
    assert result["approved"] is True
    assert result["coach_response"] == "Here is the revised schedule with more speaking..."
    assert result["reviewer_response"] == "APPROVED: Looks perfect!"
    
    # Check execution steps
    steps = result["steps"]
    assert any(s["name"] == "Reviewer Agent" and s["status"] == "success" for s in steps)

@patch("ielts_coach.workflow.validate_user_prompt")
@patch("ielts_coach.workflow.run_agent_with_retry")
@patch("ielts_coach.workflow.was_tool_called")
def test_integration_rejection_recovery_failed_after_retry(mock_was_tool_called, mock_run_agent, mock_validate):
    mock_validate.return_value = (True, "")
    mock_was_tool_called.return_value = True
    
    # First call: Coach L1 plan
    # Second call: Reviewer L1 REJECTED
    # Third call: Coach L2 revised plan
    # Fourth call: Reviewer L2 REJECTED again
    mock_run_agent.side_effect = [
        "Schedule 1",
        "REJECTED: Needs improvement",
        "Schedule 2",
        "REJECTED: Still bad"
    ]
    
    prompt = (
        "My current IELTS scores are L:6.5, R:6.5, W:6.0, S:6.5. "
        "My target scores are L:7.0, R:7.0, W:6.5, S:6.5. "
        "I want to optimize a 30-day study plan. "
        "I can study a maximum of 6.0 hours per day."
    )
    
    result = execute_study_plan_flow(prompt)
    
    assert result["approved"] is False
    assert "System unable to auto-optimize study plan" in result["coach_response"]
    assert "Still bad" in result["coach_response"]
    assert result["reviewer_response"] == "REJECTED: Still bad"
