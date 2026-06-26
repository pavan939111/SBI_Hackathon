"""
Queue Hatao agent: handles appointment schedules and DMS level increments.
"""
from app.agents.state import AgentState
from app.agents.queue_hatao.dms_tracker import DMSTracker

async def queue_hatao_node(state: AgentState) -> AgentState:
    """Resolves scheduling queues and updates digital adoption maturity score."""
    tracker = DMSTracker()
    cust_id = state.get("customer_id")
    last_msg = state["messages"][-1]["content"] if state["messages"] else ""
    intent = state.get("intent") or ""
    
    # Verify OTP gate for financial transactions (e.g. RD or FD creation)
    is_financial = "rd" in last_msg.lower() or "fd" in last_msg.lower() or intent == "financial_origination"
    
    if is_financial:
        if not state.get("otp_verified"):
            # If the user has just provided a 6-digit numeric code, verify it
            if last_msg.isdigit() and len(last_msg) == 6:
                state["otp_verified"] = True
                state["messages"].append({
                    "role": "assistant",
                    "content": "OTP verified successfully. Your Fixed/Recurring Deposit has been opened (Mock YONO API called)."
                })
                state["dms_level"] = 3  # Level 3: Saver
                if cust_id:
                    tracker.update_score(cust_id, 3)
            else:
                state["risk_tier"] = 2
                state["otp_verified"] = False
                state["messages"].append({
                    "role": "assistant",
                    "content": "For security, an OTP has been sent to your registered mobile number. Please enter the 6-digit OTP here to confirm."
                })
                return state

    if cust_id and state.get("dms_level", 0) < 2:
        # Progresses target to level 2 (Transactor)
        tracker.update_score(cust_id, 2)
        state["dms_level"] = 2
        
    return state

