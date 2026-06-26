"""
Jodo agent node logic managing conversational updates for profile data gaps.
"""
from typing import Dict, Any
from app.agents.state import AgentState
from app.agents.jodo.completeness_evaluator import CompletenessEvaluator

# Fallback messages dictionary matching v7.0 specifications
FALLBACK_MESSAGES = {
    "kyc_occupation": {
        "whatsapp": "Raju garu, mee account lo occupation mention ledu. Meeru farmer, student, or business owner? Cheppandi - profile update chestaanu.",
        "sms": "Reply OCC FARMER to update occupation to Farmer, or visit your nearest SBI branch."
    },
    "aadhaar_linked": {
        "whatsapp": "Aadhaar link chestey e-KYC complete avutundi. Mee ATM or YONO nundi 2 nimishallo cheyyochu. Request submit cheyyamantara? [Yes / No]",
        "sms": "Reply AADH to get Aadhaar linking steps, or visit branch for assisted linking."
    },
    "nominee_name": {
        "whatsapp": "Nominee add chestey mee account secure avutundi. Just name and relation cheppandi - 1 minute lo process chestaanu.",
        "sms": "Reply NOM NAME RELATION to add nominee, or visit branch."
    }
}

async def jodo_node(state: AgentState) -> AgentState:
    """
    Jodo Node: Identifies highest-priority missing profile fields and prompts
    the user conversationally to resolve the gap.
    """
    evaluator = CompletenessEvaluator()
    
    # Construct a temporary mock profile based on state declarations
    declarations = state.get("declarations") or {}
    
    mock_profile = {
        "phone_number": state.get("phone_number"),
        "aadhaar_linked": declarations.get("aadhaar_linked", False),
        "kyc_occupation": declarations.get("kyc_occupation", "Unknown"),
        "nominee_name": declarations.get("nominee_name", ""),
        "dms_level": state.get("dms_level", 0),
        "has_active_transactions": state.get("dms_level", 0) >= 2
    }
    
    # Evaluate completeness
    score, missing_fields = evaluator.evaluate(mock_profile)
    state["profile_score"] = score
    state["missing_fields"] = missing_fields
    
    if not missing_fields:
        # All fields present, skip prompts
        return state

    # Check last user message to see if they are responding to a Jodo prompt
    last_msg = state["messages"][-1]["content"] if state["messages"] else ""
    target_field = missing_fields[0]
    
    # Handle user confirmation to apply fixes
    if last_msg.lower() in ["yes", "allow", "avunu"]:
        if target_field == "kyc_occupation":
            declarations["kyc_occupation"] = "farmer" # Mock setting it to farmer
            state["messages"].append({
                "role": "assistant",
                "content": "Occupation: self-declaration recorded as Farmer ✓ (pending SBI verification)."
            })
        elif target_field == "aadhaar_linked":
            declarations["aadhaar_linked"] = True # Mock linking Aadhaar
            state["messages"].append({
                "role": "assistant",
                "content": "Aadhaar link request submitted ✓. Will be processed within 24 hours."
            })
        elif target_field == "nominee_name":
            declarations["nominee_name"] = "Sita Reddy (Wife)" # Mock nominee
            state["messages"].append({
                "role": "assistant",
                "content": "Nominee registered as Sita Reddy (Wife) ✓."
            })
            
        state["declarations"] = declarations
        # Re-evaluate after update
        mock_profile["aadhaar_linked"] = declarations.get("aadhaar_linked", False)
        mock_profile["kyc_occupation"] = declarations.get("kyc_occupation", "Unknown")
        mock_profile["nominee_name"] = declarations.get("nominee_name", "")
        
        score, missing_fields = evaluator.evaluate(mock_profile)
        state["profile_score"] = score
        state["missing_fields"] = missing_fields
        
        if not missing_fields:
            return state
        target_field = missing_fields[0]

    # Render prompt for the highest priority missing field
    # Fetch template based on context channel (default: whatsapp)
    channel = state.get("recovery_context", {}).get("channel", "whatsapp")
    msg_template = FALLBACK_MESSAGES.get(target_field, {}).get(channel, FALLBACK_MESSAGES[target_field]["whatsapp"])
    
    state["messages"].append({
        "role": "assistant",
        "content": msg_template
    })
    
    return state
