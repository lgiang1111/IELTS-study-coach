# ielts_coach/mcp_server.py
"""
MCP Server providing IELTS study schedule optimization tool over stdio transport.
"""

import json
from mcp.server.fastmcp import FastMCP
from ielts_coach.ga_engine import run_ga

# Initialize FastMCP Server
mcp = FastMCP("IELTS Study Planner")

@mcp.tool()
def optimize_schedule(initial_bands_str: str, target_bands_str: str, total_days: int) -> str:
    """
    Optimize a 7-day study schedule using Genetic Algorithm.
    
    Args:
        initial_bands_str: comma-separated initial scores for L,R,W,S (e.g., "6.0,6.5,5.5,6.0")
        target_bands_str: comma-separated target scores for L,R,W,S (e.g., "7.0,7.0,6.5,6.5")
        total_days: total study duration in days (at least 7)
    """
    try:
        init_vals = [float(x.strip()) for x in initial_bands_str.split(",")]
        target_vals = [float(x.strip()) for x in target_bands_str.split(",")]
        skills = ["L", "R", "W", "S"]
        initial_bands = dict(zip(skills, init_vals))
        target_bands = dict(zip(skills, target_vals))
        
        result = run_ga(initial_bands, target_bands, total_days)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)

if __name__ == "__main__":
    # Run the server via stdio transport (default)
    mcp.run()
