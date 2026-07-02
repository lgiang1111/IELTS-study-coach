# ielts_coach/workflow.py
"""
Workflow engine coordinating the multi-agent pipeline: Security Guardrail -> Coach Agent -> Reviewer Agent.
"""

import logging
import json
import re
from ielts_coach.agents.base import run_agent_with_retry, is_json_error
from ielts_coach.agents.security import validate_user_prompt
from ielts_coach.agents.coach import get_coach_agent, reset_tool_called, was_tool_called
from ielts_coach.agents.reviewer import get_reviewer_agent
from ielts_coach.feasibility import check_feasibility

logger = logging.getLogger("ielts_coach")

def parse_prompt_parameters(message: str) -> tuple | None:
    """
    Extract IELTS scores, days, and max study hours from user message.
    """
    init_match = re.search(r"current(?: IELTS)? scores are L:(\d+(?:\.\d+)?),\s*R:(\d+(?:\.\d+)?),\s*W:(\d+(?:\.\d+)?),\s*S:(\d+(?:\.\d+)?)", message, re.IGNORECASE)
    targ_match = re.search(r"target(?: scores)? are L:(\d+(?:\.\d+)?),\s*R:(\d+(?:\.\d+)?),\s*W:(\d+(?:\.\d+)?),\s*S:(\d+(?:\.\d+)?)", message, re.IGNORECASE)
    days_match = re.search(r"(\d+)-day", message, re.IGNORECASE)
    hours_match = re.search(r"maximum of (\d+(?:\.\d+)?) hours", message, re.IGNORECASE)

    if init_match and targ_match and days_match:
        try:
            initial = {
                "L": float(init_match.group(1)),
                "R": float(init_match.group(2)),
                "W": float(init_match.group(3)),
                "S": float(init_match.group(4))
            }
            target = {
                "L": float(targ_match.group(1)),
                "R": float(targ_match.group(2)),
                "W": float(targ_match.group(3)),
                "S": float(targ_match.group(4))
            }
            days = int(days_match.group(1))
            max_hours = float(hours_match.group(1)) if hours_match else 4.0
            return initial, target, days, max_hours
        except ValueError:
            return None
    return None

def execute_study_plan_flow(user_message: str, api_key: str = None, mock_scenario: str = None) -> dict:
    """
    Coordinates SecurityGuardrailAgent, Feasibility Check, CoachAgent, and ReviewerAgent in a sequential pipeline.
    Supports dynamic API keys and mock scenario simulations for public demos.
    """
    import time
    import os
    if mock_scenario:
        logger.info(f"[Flow] Starting Mock Demo Scenario: '{mock_scenario}'")
        from ielts_coach.mock_data import MOCK_SCENARIOS
        if mock_scenario in MOCK_SCENARIOS:
            sc_data = MOCK_SCENARIOS[mock_scenario]
            for log in sc_data["logs"]:
                logger.info(log)
                time.sleep(0.08)  # Mimic processing delays
            
            # Write simulated GA result to disk for UI visualization
            os.makedirs("logs", exist_ok=True)
            ga_res = sc_data.get("ga_result")
            if ga_res:
                try:
                    with open("logs/last_ga_result.json", "w", encoding="utf-8") as f:
                        json.dump(ga_res, f, ensure_ascii=False, indent=2)
                except Exception as write_err:
                    logger.warning(f"Failed to save mock GA result: {write_err}")
            else:
                if os.path.exists("logs/last_ga_result.json"):
                    try:
                        os.remove("logs/last_ga_result.json")
                    except:
                        pass
            
            return {
                "coach_response": sc_data["output"],
                "reviewer_response": "",
                "approved": sc_data["approved"],
                "steps": sc_data["steps"]
            }
        else:
            logger.error(f"[Flow] Unknown mock scenario: '{mock_scenario}'")
            return {
                "coach_response": f"Error: Mock scenario '{mock_scenario}' not found.",
                "reviewer_response": "",
                "approved": False,
                "steps": []
            }

    logger.info(f"[Flow] Starting execution flow. Input: '{user_message}'")
    
    # 1. RUN SECURITY GUARDRAIL
    is_valid, security_error = validate_user_prompt(user_message, api_key=api_key)
    if not is_valid:
        logger.warning(f"[Flow] Input blocked by security: {security_error}")
        steps = [
            {"name": "Security Guardrail", "status": "failed", "message": security_error},
            {"name": "Feasibility Pre-Check", "status": "skipped", "message": "Blocked by security layer."},
            {"name": "Coach Agent", "status": "skipped", "message": "Blocked by security layer."},
            {"name": "Reviewer Agent", "status": "skipped", "message": "Blocked by security layer."}
        ]
        return {
            "coach_response": f"🛡️ **Security Guardrail Alert**:\n\n{security_error}\n\n*The IELTS Study Coach only accepts queries related to IELTS preparation, study planning, or learning strategies. Unrelated prompts or system intervention attempts will be blocked.*",
            "reviewer_response": "",
            "approved": False,
            "steps": steps
        }
        
    steps = [
        {"name": "Security Guardrail", "status": "success", "message": "Checked: Safe & Valid."}
    ]
 
    # 1.5. FEASIBILITY CHECK
    params = parse_prompt_parameters(user_message)
    if params:
        initial, target, days, max_hours = params
        feasibility = check_feasibility(initial, target, days, max_hours)
        if not feasibility["feasible"]:
            logger.warning(f"[Flow] Input goals are mathematically infeasible: {feasibility}")
            
            required_h = feasibility["required_hours"]
            avail_h = feasibility["available_hours"]
            sug_days = feasibility.get("suggested_days", days)
            sug_hours = feasibility.get("suggested_daily_hours", max_hours)
            
            error_response = (
                f"⚠️ **Infeasible Study Target (Feasibility Warning)**\n\n"
                f"Based on the exponential learning curve, your target score increase requires approximately **{required_h} hours** of dedicated study. "
                f"However, with your current settings ({days} days, max {max_hours} hours/day), you only have a maximum of **{avail_h} hours** available.\n\n"
                f"👉 **Recommended Adjustments (Human-in-the-Loop):**\n"
                f"- **Increase total study days** to at least **{sug_days} days** (retaining {max_hours} hours/day).\n"
                f"- **Or increase daily study hours** to at least **{sug_hours} hours/day** (retaining {days} days).\n"
                f"- **Or reduce target band scores** to match realistic expectations.\n\n"
                f"*Please adjust the slider parameters in the sidebar and click Optimize Schedule again.*"
            )
            
            steps.append({
                "name": "Feasibility Pre-Check", 
                "status": "failed", 
                "message": f"Infeasible: Requires {required_h}h, available {avail_h}h."
            })
            steps.append({"name": "Coach Agent", "status": "skipped", "message": "Skipped due to infeasibility."})
            steps.append({"name": "Reviewer Agent", "status": "skipped", "message": "Skipped due to infeasibility."})
            
            return {
                "coach_response": error_response,
                "reviewer_response": "",
                "approved": False,
                "steps": steps
            }
        else:
            steps.append({
                "name": "Feasibility Pre-Check", 
                "status": "success", 
                "message": f"Feasible: Requires {feasibility['required_hours']}h, available {feasibility['available_hours']}h."
            })
    else:
        steps.append({
            "name": "Feasibility Pre-Check", 
            "status": "success", 
            "message": "Skipped (No schedule generation request detected)."
        })
    
    # 2. RUN COACH AGENT
    logger.info("[Flow] Invoking CoachAgent...")
    reset_tool_called()
    coach = get_coach_agent(api_key=api_key)
    coach_content = run_agent_with_retry(coach, user_message)
    logger.info("[Flow] CoachAgent completed.")
    
    # Handle Coach error
    if is_json_error(coach_content):
        logger.error(f"[Flow] CoachAgent failed with model/gateway error: {coach_content}")
        try:
            error_data = json.loads(coach_content)
            err_msg = error_data["error"].get("message", "Model unavailable.")
        except:
            err_msg = "Model unavailable."
            
        steps.append({"name": "Coach Agent", "status": "failed", "message": f"System error: {err_msg}"})
        steps.append({"name": "Reviewer Agent", "status": "skipped", "message": "Skipped due to Coach Agent failure."})
        return {
            "coach_response": f"❌ **System Error**: Coach Agent is currently unavailable (Error: {err_msg}). Please try again in a few minutes.",
            "reviewer_response": "",
            "approved": False,
            "steps": steps
        }
        
    has_schedule = was_tool_called()
    
    # 3. RUN REVIEWER AGENT (IF SCHEDULE WAS GENERATED)
    review_content = ""
    approved = True
    
    if has_schedule:
        steps.append({"name": "Coach Agent", "status": "success", "message": "Optimized schedule using GA."})
        
        logger.info("[Flow] Proposed schedule detected. Invoking ReviewerAgent...")
        reviewer = get_reviewer_agent(api_key=api_key)
        review_content = run_agent_with_retry(
            reviewer,
            f"Please review this proposed study schedule and explain your verdict:\n\n{coach_content}"
        )
        logger.info("[Flow] ReviewerAgent completed.")
        
        # Handle Reviewer error
        if is_json_error(review_content):
            logger.error(f"[Flow] ReviewerAgent failed: {review_content}")
            try:
                error_data = json.loads(review_content)
                err_msg = error_data["error"].get("message", "Model unavailable.")
            except:
                err_msg = "Model unavailable."
                
            steps.append({"name": "Reviewer Agent", "status": "failed", "message": f"Could not evaluate: {err_msg}"})
            return {
                "coach_response": coach_content,
                "reviewer_response": f"❌ **Pedagogical Reviewer Error**: Reviewer Agent is temporarily unresponsive (Error: {err_msg}). Your study schedule was still generated, please assess it manually.",
                "approved": False,
                "steps": steps
            }
            
        logger.info(f"[Flow] ReviewerAgent verdict: {review_content[:50]}...")
        
        if "REJECTED" in review_content.upper():
            logger.info("[Flow] Plan REJECTED by reviewer. Initiating automatic retry...")
            steps.append({"name": "Reviewer Agent", "status": "warning", "message": "Attempt 1 rejected. Self-healing retry triggered..."})
            
            retry_message = (
                f"The study schedule you proposed earlier was rejected by the Reviewer Agent for the following reason:\n\n"
                f"\"{review_content}\"\n\n"
                f"Please generate a new study schedule using 'optimize_schedule_tool' and "
                f"adjust it to address the pedagogical concerns mentioned above."
            )
            
            logger.info("[Flow] Running CoachAgent retry attempt...")
            reset_tool_called()
            coach_content_retry = run_agent_with_retry(coach, retry_message)
            
            if was_tool_called():
                logger.info("[Flow] Retry generated schedule. Reviewing again...")
                review_content_retry = run_agent_with_retry(
                    reviewer,
                    f"Please review this revised study schedule and explain your verdict:\n\n{coach_content_retry}"
                )
                
                if "REJECTED" in review_content_retry.upper():
                    approved = False
                    logger.info("[Flow] Plan REJECTED again on retry.")
                    
                    hitl_response = (
                        f"{coach_content_retry}\n\n"
                        f"---\n"
                        f"🚨 **System unable to auto-optimize study plan to meet reviewer standards**\n"
                        f"Reviewer Agent rejected the retry with this response:\n"
                        f"> *{review_content_retry}*\n\n"
                        f"👉 **Recommended Adjustments (Human-in-the-Loop):**\n"
                        f"To generate a valid schedule, please try to:\n"
                        f"- Lower your target band scores slightly (e.g., by 0.5 band).\n"
                        f"- Or increase total study days in the sidebar.\n"
                        f"- Or increase maximum daily study hours."
                    )
                    
                    steps.append({
                        "name": "Reviewer Agent", 
                        "status": "failed", 
                        "message": "Attempt 2 rejected. Human-in-the-loop adjustments required."
                    })
                    
                    return {
                        "coach_response": hitl_response,
                        "reviewer_response": review_content_retry,
                        "approved": False,
                        "steps": steps
                    }
                else:
                    logger.info("[Flow] Plan APPROVED on retry.")
                    steps.append({
                        "name": "Reviewer Agent", 
                        "status": "success", 
                        "message": "Approved after self-healing retry."
                    })
                    return {
                        "coach_response": coach_content_retry,
                        "reviewer_response": review_content_retry,
                        "approved": True,
                        "steps": steps
                    }
            else:
                logger.info("[Flow] Retry did not trigger GA tool.")
                steps.append({
                    "name": "Reviewer Agent", 
                    "status": "failed", 
                    "message": "Retry did not generate a new schedule."
                })
                return {
                    "coach_response": coach_content_retry,
                    "reviewer_response": "Retry failed to invoke scheduling tool.",
                    "approved": False,
                    "steps": steps
                }
        else:
            logger.info("[Flow] Plan APPROVED by reviewer.")
            steps.append({"name": "Reviewer Agent", "status": "success", "message": "Evaluated: Approved and pedagogically sound."})
    else:
        steps.append({"name": "Coach Agent", "status": "success", "message": "Completed chat response."})
        steps.append({"name": "Reviewer Agent", "status": "skipped", "message": "Skipped (No schedule generated)."})
        
    return {
        "coach_response": coach_content,
        "reviewer_response": review_content,
        "approved": approved,
        "steps": steps
    }

