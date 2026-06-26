import os
import json
import logging
from app.agents.state import AgentState
from app.services.gemini import GeminiService
from app.agents.samjho.intent_classifier import IntentClassifier
from app.agents.samjho.language_detector import LanguageDetector
from app.db.postgres import AsyncSessionLocal
from app.services.audit import AuditService

logger = logging.getLogger("banksaathi.samjho")

async def samjho_node(state: AgentState) -> AgentState:
    """Classifies user input, extracts parameters and updates system state."""
    text_content = state["messages"][-1]["content"] if state["messages"] else ""
    
    # 1. Classify intent and language using Gemini
    gemini = GeminiService()
    prompt_path = os.path.join(os.path.dirname(__file__), "../../../prompts/samjho_system.txt")
    system_prompt = ""
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
            
    if system_prompt:
        full_prompt = f"{system_prompt}\n\nUser Message: {text_content}\n\nReturn raw JSON only:"
        try:
            response_text = await gemini.get_chat_response(full_prompt)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
                
            parsed = json.loads(response_text.strip())
            state["intent"] = parsed.get("intent", "general_query")
            state["language"] = parsed.get("language", "en")
            state["risk_tier"] = parsed.get("risk_tier", 1)
        except Exception as e:
            logger.warning(f"Gemini LLM call failed in Samjho: {e}. Falling back to rule-based parser.")
            state["language"] = LanguageDetector().detect(text_content)
            state["intent"] = IntentClassifier().classify(text_content)
            state["risk_tier"] = 1
    else:
        state["language"] = LanguageDetector().detect(text_content)
        state["intent"] = IntentClassifier().classify(text_content)
        state["risk_tier"] = 1

    # 2. Log compliance operations (AI Disclosure & Consent)
    audit_service = AuditService()
    cust_id = state.get("customer_id")
    sess_id = state.get("recovery_context", {}).get("session_id")
    
    # Set default declarations if missing
    if "declarations" not in state:
        state["declarations"] = {}

    async with AsyncSessionLocal() as session:
        # Step 0: Log AI disclosure presentation
        await audit_service.log_action(
            db=session,
            session_id=sess_id,
            customer_id=cust_id,
            agent_name="Samjho",
            action_type="AI_Disclosure_Presented",
            action_detail={"message": "Mandatory AI Disclosure displayed to customer."},
            risk_tier=1,
            autonomous=True,
            outcome="success"
        )
        
        # Step 1: Capture consent dynamically if user replies "allow" or "yes" or consent exists
        consent_reply = text_content.lower() in ["allow", "yes", "avunu", "accept"]
        if consent_reply:
            state["declarations"]["consent_granted"] = True
            await audit_service.log_action(
                db=session,
                session_id=sess_id,
                customer_id=cust_id,
                agent_name="Samjho",
                action_type="Consent_Granted",
                action_detail={"scope": ["account_type", "transaction_pattern", "land_records"]},
                risk_tier=1,
                autonomous=True,
                outcome="success"
            )

    return state

