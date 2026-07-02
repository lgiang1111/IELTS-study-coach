# tests/test_agents.py
import pytest
import os
import json
from ielts_coach.agents.base import get_model
from ielts_coach.agents.coach import get_coach_agent
from ielts_coach.agents.reviewer import get_reviewer_agent
from ielts_coach.workflow import execute_study_plan_flow
from ielts_coach.mcp_server import optimize_schedule

def test_model_factory():
    model = get_model()
    assert model is not None
    assert hasattr(model, "id")

def test_agents_initialization():
    coach = get_coach_agent()
    reviewer = get_reviewer_agent()
    
    assert coach.name == "IELTS Coach"
    assert reviewer.name == "IELTS Reviewer"
    assert len(coach.instructions) > 0
    assert len(reviewer.instructions) > 0

def test_mcp_tool_direct_call():
    result_str = optimize_schedule("6.0,6.0,6.0,6.0", "7.0,7.0,7.0,7.0", 30)
    result = json.loads(result_str)
    
    assert result["status"] == "success"
    assert "schedule" in result
    assert "forecasted_scores" in result
    assert len(result["schedule"]) == 7

def test_execute_study_plan_flow_integration():
    # Only run if a base URL or api key is available, else skip or mock
    if not os.getenv("LITELLM_BASE_URL") and not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No LLM key or gateway available for integration test")
        
    prompt = (
        "My current IELTS bands are L:6.5, R:6.0, W:5.5, S:6.0. "
        "I want to reach 7.0 in L/R and 6.5 in W/S. I have 30 days to study. "
        "Please generate an optimized study schedule."
    )
    
    result = execute_study_plan_flow(prompt)
    
    assert "coach_response" in result
    assert "reviewer_response" in result
    assert "approved" in result
    assert len(result["coach_response"]) > 0
    
    # Check if log file was created and contains logs
    assert os.path.exists("logs/agent.log")
    with open("logs/agent.log", "r", encoding="utf-8") as f:
        logs = f.read()
        assert "[Flow] Starting execution flow" in logs
        assert "Invoking CoachAgent" in logs
