"""
Chalao agent: guides the customer step-by-step through YONO app interfaces.
"""
from app.agents.state import AgentState
from app.agents.chalao.yono_navigator import YONONavigator

async def chalao_node(state: AgentState) -> AgentState:
    """
    Chalao Node: Prepares step-by-step YONO navigation, guides form inputs,
    and handles recovery fallbacks if the user gets lost.
    """
    schemes = state.get("matched_schemes", [])
    last_msg = state["messages"][-1]["content"].lower() if state["messages"] else ""
    
    # 1. Recovery Trigger: User states they are on a different/wrong screen
    if "different" in last_msg or "wrong" in last_msg or "ledu" in last_msg:
        state["messages"].append({
            "role": "assistant",
            "content": "괜찮ా (No problem) - idi common. Oka pani cheyyandi: screenshot teesukooni ikkade send cheyyandi. Nenu correct screen ki guide chestanu."
        })
        state["recovery_context"]["wrong_screen_state"] = True
        return state

    # 2. Recovery Trigger: User sends a simulated screenshot file payload
    if state.get("recovery_context", {}).get("wrong_screen_state") and ("png" in last_msg or "jpg" in last_msg or "[image]" in last_msg or "screenshot" in last_msg):
        # Reset flag and direct them back to correct path
        state["recovery_context"]["wrong_screen_state"] = False
        state["messages"].append({
            "role": "assistant",
            "content": "Got it - I see you are on the 'Accounts' screen. Let's redirect: tap 'More' (bottom right) -> 'Loans' -> 'Kisan Credit Card' to resume."
        })
        return state

    # 3. Recovery Trigger: User explicitly states frustration or inability to do it
    if "lost" in last_msg or "cannot" in last_msg or "help" in last_msg or "artham" in last_msg:
        state["messages"].append({
            "role": "assistant",
            "content": "No problem. Rendu options unnai:\n\nOption 1: Nenu branch appointment book chestanu - officer YONO setup chestaru. [Book now]\nOption 2: Call YONO helpline: 1800-11-2211."
        })
        return state

    # Normal Happy Path
    if schemes:
        navigator = YONONavigator()
        steps = navigator.get_steps(schemes[0])
        state["form_prefilled"] = {
            "navigation_steps": steps,
            "prefilled_fields": {"account_number": "XXXX7823", "kyc_status": "verified"}
        }
        
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        state["messages"].append({
            "role": "assistant",
            "content": f"Chalao co-pilot active. Here are your navigation steps:\n{steps_text}\n\nPre-filled: Account number and land vault references. Please tap Confirm on your screen to complete application."
        })
        
    return state

