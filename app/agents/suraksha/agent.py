import os
import logging
from app.agents.state import AgentState
from app.agents.suraksha.anomaly_detector import AnomalyDetector
from app.services.gemini import GeminiService

logger = logging.getLogger("banksaathi.suraksha")

async def suraksha_node(state: AgentState) -> AgentState:
    """Scans operations for fraud indicators and executes security gating rules."""
    text_content = state["messages"][-1]["content"] if state["messages"] else ""
    detector = AnomalyDetector()
    
    is_anomaly = detector.scan_activity(text_content) or state.get("intent") == "fraud_alert"
    
    if is_anomaly:
        state["risk_tier"] = 3
        state["requires_officer"] = True
        
        gemini = GeminiService()
        prompt_path = os.path.join(os.path.dirname(__file__), "../../../prompts/suraksha_system.txt")
        system_prompt = ""
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
                
        warning_msg = "SBI NEVER asks for OTPs or PINs over a call. This message is highly suspicious and appears to be a scam. Please contact SBI helpline immediately at 1800-11-2211."
        if system_prompt:
            full_prompt = (
                f"{system_prompt}\n\n"
                f"User Message: {text_content}\n"
                f"Generate a clear security warning response advising the customer to stay safe:"
            )
            try:
                response = await gemini.get_chat_response(full_prompt)
                warning_msg = response.strip()
            except Exception as e:
                logger.warning(f"Gemini call failed in Suraksha: {e}. Using fallback warning.")
                
        state["messages"].append({
            "role": "assistant",
            "content": f"[ALERT - TIER 3 RISK DETECTED]\n\n{warning_msg}"
        })
        
    return state

