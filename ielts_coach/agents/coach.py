# ielts_coach/agents/coach.py
"""
IELTS Coach Agent (Planner & Advisor) with Genetic Algorithm and Web Search skills.
"""

import os
import json
import logging
import urllib.request
import urllib.parse
from agno.agent import Agent
from ielts_coach.agents.base import get_model
from ielts_coach.ga_engine import run_ga

logger = logging.getLogger("ielts_coach")

_optimize_schedule_tool_called = False

def reset_tool_called() -> None:
    global _optimize_schedule_tool_called
    _optimize_schedule_tool_called = False

def was_tool_called() -> bool:
    global _optimize_schedule_tool_called
    return _optimize_schedule_tool_called

def optimize_schedule_tool(initial_bands_str: str, target_bands_str: str, total_days: int) -> str:
    """
    Optimize a 7-day IELTS study schedule using Genetic Algorithm.
    
    Args:
        initial_bands_str: comma-separated initial scores for L,R,W,S (e.g. "6.0, 6.5, 5.5, 6.0")
        target_bands_str: comma-separated target scores for L,R,W,S (e.g. "7.0, 7.0, 6.5, 6.5")
        total_days: total study duration in days (must be >= 7)
    """
    global _optimize_schedule_tool_called
    _optimize_schedule_tool_called = True
    logger.info(f"[Coach Skill] GA Tool called with initial={initial_bands_str}, target={target_bands_str}, days={total_days}")
    try:
        init_vals = [float(x.strip()) for x in initial_bands_str.split(",")]
        target_vals = [float(x.strip()) for x in target_bands_str.split(",")]
        skills = ["L", "R", "W", "S"]
        initial_bands = dict(zip(skills, init_vals))
        target_bands = dict(zip(skills, target_vals))
        
        result = run_ga(initial_bands, target_bands, total_days)
        logger.info(f"[Coach Skill] GA optimization complete. Fitness={result.get('fitness')}")
        
        # Save last result for UI/CLI consumption
        try:
            with open("logs/last_ga_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as write_err:
            logger.warning(f"Failed to save last GA result: {write_err}")
            
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        error_msg = f"GA Tool Error: {str(e)}"
        logger.error(error_msg)
        return json.dumps({"status": "error", "message": error_msg})

def searxng_search_tool(query: str) -> str:
    """
    Search the web for up-to-date information on IELTS exam formats, tips, test criteria, or general questions using SearXNG.
    
    Args:
        query: search query string
    """
    url = os.getenv("SEARXNG_URL", "http://172.20.0.26:8888")
    logger.info(f"[Coach Skill] SearXNG Search Tool called with query: '{query}'")
    try:
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"{url.rstrip('/')}/search?q={encoded_query}&format=json"
        
        req = urllib.request.Request(
            search_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get("results", [])
            
            # Format top 5 results nicely
            formatted = []
            for r in results[:5]:
                title = r.get("title", "No Title")
                link = r.get("url", "")
                content = r.get("content", "")
                formatted.append(f"Title: {title}\nLink: {link}\nSnippet: {content}\n")
                
            if not formatted:
                logger.info(f"[Coach Skill] SearXNG returned no results.")
                return "No search results found."
            
            logger.info(f"[Coach Skill] SearXNG search success. Retrieved {len(formatted)} results.")
            return "\n".join(formatted)
    except Exception as e:
        error_msg = f"SearXNG Search failed: {str(e)}"
        logger.error(error_msg)
        return error_msg

def get_coach_agent(session_id: str = None, api_key=None) -> Agent:
    """
    Return the IELTS Study Coach Agent (Planner).
    """
    return Agent(
        name="IELTS Coach",
        role="IELTS Study Planner & Advisor",
        model=get_model(api_key),
        instructions=[
            "You are an expert IELTS Coach helper.",
            "If the user requests to create or optimize a study plan, ALWAYS call 'optimize_schedule_tool'.",
            "Do NOT make up schedule data. Always rely on the tool output.",
            "If the user asks general questions about IELTS tips, band descriptors, format, or study resources, you can use the 'searxng_search_tool' to search the web for current, accurate information.",
            "Format your final response cleanly, explaining the study plan and predicted scores. Make sure to present your findings nicely with markdown."
        ],
        tools=[optimize_schedule_tool, searxng_search_tool],
        telemetry=False
    )
