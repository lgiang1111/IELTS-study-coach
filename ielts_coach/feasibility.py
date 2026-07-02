# ielts_coach/feasibility.py
"""
Feasibility checker module to pre-validate user IELTS prep goals.
Prevents unachievable schedules from running expensive GA runs.
"""

import math

def check_feasibility(
    initial_bands: dict[str, float],
    target_bands: dict[str, float],
    total_days: int,
    max_daily_hours: float
) -> dict:
    """
    Check if the target IELTS scores are mathematically achievable.
    
    Args:
        initial_bands: dictionary of initial scores (L, R, W, S)
        target_bands: dictionary of target scores (L, R, W, S)
        total_days: study duration in days (must be >= 7)
        max_daily_hours: max hours user can study daily (must be > 0)
        
    Returns:
        dict: feasibility status, required hours, available hours, and recommended adjustments
    """
    if total_days <= 0:
        raise ValueError("Total study days must be greater than 0.")
    if max_daily_hours <= 0.0:
        raise ValueError("Max daily hours must be greater than 0.")

    # Learning rate (k) per skill from ga_engine.py
    k_rates = {
        "L": 0.006,
        "R": 0.005,
        "W": 0.003,
        "S": 0.004
    }

    total_req_hours = 0.0
    details = {}

    for skill in ["L", "R", "W", "S"]:
        p0 = initial_bands.get(skill, 6.0)
        pn = target_bands.get(skill, 6.0)

        if pn <= p0:
            req_t = 0.0
        else:
            # Clip target at 8.9 to avoid division by zero or negative log for target score of 9.0
            pn_capped = min(pn, 8.9)
            k = k_rates[skill]
            # Inverted learning curve: t = (1/k) * ln((9.0 - p0) / (9.0 - pn))
            req_t = (1.0 / k) * math.log((9.0 - p0) / (9.0 - pn_capped))

        total_req_hours += req_t
        details[skill] = round(req_t, 1)

    # Max weekly hours in GA: 24 blocks of 2h = 48 hours
    max_weekly_hours = min(48.0, 7.0 * max_daily_hours)
    total_avail_hours = max_weekly_hours * (total_days / 7.0)

    feasible = total_avail_hours >= total_req_hours

    res = {
        "feasible": feasible,
        "required_hours": round(total_req_hours, 1),
        "available_hours": round(total_avail_hours, 1),
        "details": details
    }

    if not feasible:
        # 1. Suggest more prep days
        # Days needed = (required_hours / max_weekly_hours) * 7
        needed_days = math.ceil((total_req_hours / max_weekly_hours) * 7.0)
        res["suggested_days"] = max(needed_days, total_days + 5)

        # 2. Suggest higher max daily hours
        # Daily hours = (required_hours / (total_days / 7.0)) / 7.0 = required_hours / total_days
        needed_daily_hours = math.ceil((total_req_hours / total_days) * 2) / 2.0  # round to nearest 0.5
        res["suggested_daily_hours"] = min(needed_daily_hours, 8.0)

    return res
