# ielts_coach/agents/base.py
"""
Common base configurations, model factory, and resilient invocation wrapper for IELTS Coach agents.
"""

import os
import time
import logging
from dotenv import load_dotenv
from agno.agent import Agent, RunOutput

# Load environment variables
load_dotenv()

# Setup logging
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("ielts_coach")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers
if not logger.handlers:
    handler = logging.FileHandler("logs/agent.log", mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)

def get_model(api_key=None):
    """
    Adaptive model factory:
    1. Checks LiteLLM workspace gateway.
    2. Checks GEMINI_API_KEY environment variable.
    3. Falls back to OpenAI compatibility.
    """
    base_url = os.getenv("LITELLM_BASE_URL")
    lite_api_key = os.getenv("LITELLM_API_KEY")
    gemini_key = api_key or os.getenv("GEMINI_API_KEY")
    
    if base_url:
        from agno.models.openai import OpenAIChat
        logger.info(f"Using LiteLLM Gateway model at {base_url}")
        return OpenAIChat(
            id=os.getenv("OMNI_MAIN_MODEL", "daily"),
            base_url=base_url,
            api_key=lite_api_key or "anything"
        )
    elif gemini_key:
        from agno.models.google import Gemini
        logger.info("Using standard Gemini model (gemini-2.5-flash)")
        return Gemini(id="gemini-2.5-flash", api_key=gemini_key)
    else:
        from agno.models.openai import OpenAIChat
        logger.info("Using default OpenAI model fallback")
        return OpenAIChat(id="gpt-4o-mini")

def is_json_error(content: str) -> bool:
    if not content:
        return False
    try:
        import json
        data = json.loads(content)
        return isinstance(data, dict) and "error" in data
    except:
        content_stripped = content.strip()
        if content_stripped.startswith("{") and '"error"' in content_stripped:
            return True
        return False

def run_agent_with_retry(agent: Agent, message: str, max_retries: int = 3) -> str:
    import json
    delay = 2
    for attempt in range(max_retries):
        try:
            logger.info(f"Running agent {agent.name} (attempt {attempt + 1})...")
            run_output: RunOutput = agent.run(message)
            content = run_output.content
            
            # Check if the content itself is a JSON error from the provider/gateway
            if is_json_error(content):
                logger.warning(f"Agent {agent.name} returned provider error: {content}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
            return content
        except Exception as e:
            logger.error(f"Error running agent {agent.name} (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return json.dumps({"error": {"code": 500, "message": str(e), "status": "INTERNAL"}})
    return json.dumps({"error": {"code": 503, "message": "Failed after max retries due to model unavailability.", "status": "UNAVAILABLE"}})
