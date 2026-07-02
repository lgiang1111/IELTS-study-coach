# ielts_coach/agents/reviewer.py
"""
IELTS Pedagogical Reviewer Agent (Judge) definition.
"""

import logging
from agno.agent import Agent
from ielts_coach.agents.base import get_model

logger = logging.getLogger("ielts_coach")

def get_reviewer_agent(api_key=None) -> Agent:
    """
    Return the IELTS Pedagogical Reviewer Agent (Judge).
    """
    return Agent(
        name="IELTS Reviewer",
        role="Pedagogical Judge",
        model=get_model(api_key),
        instructions=[
            "You are an expert IELTS Pedagogical Reviewer.",
            "You review proposed study schedules and forecasted scores.",
            "Ensure the plan has a balanced distribution of skills (L, R, W, S) and is realistic.",
            "If the plan is pedagogically sound, start your response with 'APPROVED'.",
            "If there are issues, state them clearly and start with 'REJECTED'."
        ],
        telemetry=False
    )
