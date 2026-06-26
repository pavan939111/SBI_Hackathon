import os
import logging
from app.agents.state import AgentState
from app.agents.khojo.eligibility_engine import EligibilityEngine
from app.services.gemini import GeminiService

logger = logging.getLogger("banksaathi.khojo")

async def khojo_node(state: AgentState) -> AgentState:
    """Scans and matches applicable financial schemes for the user."""
    declarations = state.get("declarations") or {}
    
    mock_profile = {
        "phone_number": state.get("phone_number"),
        "aadhaar_linked": declarations.get("aadhaar_linked", False),
        "kyc_occupation": declarations.get("kyc_occupation", "Unknown"),
        "nominee_name": declarations.get("nominee_name", ""),
        "dms_level": state.get("dms_level", 0)
    }
    
    engine = EligibilityEngine()
    eligible_schemes = engine.evaluate_customer_eligibility(mock_profile)
    state["matched_schemes"] = eligible_schemes
    
    if eligible_schemes:
        # Prompt Gemini to explain why they qualify based on system guidelines
        gemini = GeminiService()
        prompt_path = os.path.join(os.path.dirname(__file__), "../../../prompts/khojo_system.txt")
        system_prompt = ""
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
                
        explanation = "You qualify for Kisan Credit Card because we found your verified land details and occupation matching farmer criteria."
        if system_prompt:
            full_prompt = (
                f"{system_prompt}\n\n"
                f"Customer Profile: {mock_profile}\n"
                f"Matched Schemes: {eligible_schemes}\n"
                f"Generate a clear, brief explainability snapshot for this customer:"
            )
            try:
                response = await gemini.get_chat_response(full_prompt)
                explanation = response.strip()
            except Exception as e:
                logger.warning(f"Gemini call failed in Khojo: {e}. Falling back to default explanation.")
                
        state["messages"].append({
            "role": "assistant",
            "content": f"Khojo found eligible schemes: {', '.join(eligible_schemes)}.\n\nExplainability: {explanation}"
        })
    else:
        # Jodo evaluator missing fields lookup will be handled by graph conditional routing
        pass
        
    return state

