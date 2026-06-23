"""
Khojo agent: running scheme lookups based on land holdings, KYC and status.
"""
from app.agents.state import AgentState
from app.agents.khojo.eligibility_engine import EligibilityEngine

async def khojo_node(state: AgentState) -> AgentState:
    """Scans and matches applicable financial schemes for the user."""
    # TODO: retrieve client customer info from DB context
    engine = EligibilityEngine()
    eligible_schemes = engine.evaluate_customer_eligibility(state.get("customer_id"))
    state["matched_schemes"] = eligible_schemes
    return state
