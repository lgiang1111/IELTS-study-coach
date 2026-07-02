# tests/test_ga.py
import pytest
import math
from ielts_coach.ga_engine import (
    calculate_learning_gain,
    calculate_fatigue,
    calculate_fitness,
    run_ga
)

def test_calculate_learning_gain_edge_cases():
    # t = 0 -> gain = p0
    assert calculate_learning_gain(6.0, 0, 0.005) == 6.0
    
    # k = 0 -> gain = p0
    assert calculate_learning_gain(6.0, 100, 0.0) == 6.0
    
    # t large -> gain close to p_inf (9.0)
    assert math.isclose(calculate_learning_gain(6.0, 100000, 0.005), 9.0, abs_tol=1e-3)

def test_calculate_learning_gain_normal():
    # p0 = 6.0, t = 100, k = 0.005. Pn = 9.0 - (9.0 - 6.0) * e^(-0.005 * 100)
    # Pn = 9.0 - 3.0 * e^(-0.5) = 9.0 - 3.0 * 0.60653 = 9.0 - 1.8196 = 7.1804
    expected = 9.0 - 3.0 * math.exp(-0.005 * 100)
    assert math.isclose(calculate_learning_gain(6.0, 100, 0.005), expected, abs_tol=1e-5)

def test_calculate_fatigue_empty():
    assert calculate_fatigue([]) == 0.0

def test_calculate_fatigue_single_block():
    # Single block of Listening (C_L = 1.2), duration 1.0 hour, alpha = 1.3
    # raw fatigue = 1.2 * 1.0^1.3 = 1.2
    schedule = [[("L", 1.0)]]
    assert math.isclose(calculate_fatigue(schedule, alpha=1.3, beta=0.2), 1.2, abs_tol=1e-5)

def test_calculate_fatigue_multiple_blocks():
    # Day 1: L (1.0), L (1.0) -> same skill, raw fatigue = 1.2*1.0^1.3 + 1.2*1.0^1.3 - 0 = 2.4
    # Day 2: L (1.0), R (1.0) -> different skills, raw fatigue = 1.2*1.0^1.3 + 1.3*1.0^1.3 - 0.2 = 1.2 + 1.3 - 0.2 = 2.3
    schedule = [
        [("L", 1.0), ("L", 1.0)],
        [("L", 1.0), ("R", 1.0)]
    ]
    # For day 1: 1.2*1^1.3 + 1.2*1^1.3 - 0 = 2.4
    # For day 2: 1.2*1^1.3 + 1.3*1^1.3 - 0.2 = 2.3
    # Total fatigue = 2.4 + 2.3 = 4.7
    assert math.isclose(calculate_fatigue(schedule, alpha=1.3, beta=0.2), 4.7, abs_tol=1e-5)

def test_calculate_fitness():
    initial_bands = {"L": 6.0, "R": 6.0, "W": 6.0, "S": 6.0}
    target_bands = {"L": 7.0, "R": 7.0, "W": 7.0, "S": 7.0}
    
    # Empty schedule should be heavily penalized
    empty_sched = [[] for _ in range(7)]
    fit_empty = calculate_fitness(empty_sched, initial_bands, target_bands)
    
    # Valid schedule should have a higher fitness
    # 4 blocks of each skill in 7 days
    valid_sched = [
        [("L", 1.0), ("R", 1.0)],
        [("W", 1.0), ("S", 1.0)],
        [("L", 1.0), ("R", 1.0)],
        [("W", 1.0), ("S", 1.0)],
        [("L", 1.0), ("R", 1.0)],
        [("W", 1.0), ("S", 1.0)],
        [("L", 1.0), ("R", 1.0), ("W", 1.0), ("S", 1.0)]
    ]
    fit_valid = calculate_fitness(valid_sched, initial_bands, target_bands)
    
    # Valid schedule must be much better than empty schedule
    assert fit_valid > fit_empty

def test_run_ga():
    initial_bands = {"L": 6.0, "R": 6.0, "W": 6.0, "S": 6.0}
    target_bands = {"L": 7.0, "R": 7.0, "W": 7.0, "S": 7.0}
    
    result = run_ga(initial_bands, target_bands, total_days=30, pop_size=50, generations=10)
    
    assert "status" in result
    assert "schedule" in result
    assert "forecasted_scores" in result
    assert "fitness" in result
    
    schedule = result["schedule"]
    assert len(schedule) == 7  # 7-day cycle
    
    for day in schedule:
        assert isinstance(day, list)
        assert len(day) <= 4  # max blocks per day is 4
        for session in day:
            assert len(session) == 2
            skill, duration = session
            assert skill in ["L", "R", "W", "S"]
            assert duration >= 0.75  # minimum block size
