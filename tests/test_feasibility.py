# tests/test_feasibility.py
import pytest
from ielts_coach.feasibility import check_feasibility

def test_feasibility_achievable():
    initial = {"L": 6.5, "R": 6.5, "W": 6.0, "S": 6.5}
    target = {"L": 7.0, "R": 7.0, "W": 6.5, "S": 6.5}
    # Available hours: min(48.0, 7.0*5.0) * 30 / 7.0 = 35.0 * 30 / 7.0 = 150 hours
    # Required hours is around 142.6 hours.
    result = check_feasibility(initial, target, total_days=30, max_daily_hours=5.0)
    
    assert result["feasible"] is True
    assert result["required_hours"] > 0.0
    assert result["available_hours"] >= result["required_hours"]

def test_feasibility_impossible():
    initial = {"L": 5.0, "R": 5.0, "W": 5.0, "S": 5.0}
    target = {"L": 8.0, "R": 8.0, "W": 8.0, "S": 8.0}
    # Clearly impossible in 10 days with 2 hours per day
    result = check_feasibility(initial, target, total_days=10, max_daily_hours=2.0)
    
    assert result["feasible"] is False
    assert "suggested_days" in result
    assert "suggested_daily_hours" in result
    assert result["suggested_days"] > 10

def test_feasibility_edge_cases():
    initial = {"L": 6.0, "R": 6.0, "W": 6.0, "S": 6.0}
    target = {"L": 6.0, "R": 6.0, "W": 6.0, "S": 6.0}
    # Target same as initial -> 0 hours required -> feasible
    result = check_feasibility(initial, target, total_days=7, max_daily_hours=1.0)
    assert result["feasible"] is True
    assert result["required_hours"] == 0.0
    
    # Target lower than initial -> 0 hours required -> feasible
    target_lower = {"L": 5.5, "R": 5.5, "W": 5.5, "S": 5.5}
    result_lower = check_feasibility(initial, target_lower, total_days=7, max_daily_hours=1.0)
    assert result_lower["feasible"] is True
    assert result_lower["required_hours"] == 0.0

def test_feasibility_clip_target():
    initial = {"L": 6.0, "R": 6.0, "W": 6.0, "S": 6.0}
    target_high = {"L": 9.0, "R": 9.0, "W": 9.0, "S": 9.0}
    # Capped target at 8.9 to avoid infinity log
    result = check_feasibility(initial, target_high, total_days=30, max_daily_hours=4.0)
    assert result["required_hours"] > 0.0
    assert result["required_hours"] < float("inf")

def test_feasibility_invalid_inputs():
    initial = {"L": 6.0, "R": 6.0, "W": 6.0, "S": 6.0}
    target = {"L": 7.0, "R": 7.0, "W": 7.0, "S": 7.0}
    with pytest.raises(ValueError):
        check_feasibility(initial, target, total_days=0, max_daily_hours=4.0)
    with pytest.raises(ValueError):
        check_feasibility(initial, target, total_days=30, max_daily_hours=-1.0)
