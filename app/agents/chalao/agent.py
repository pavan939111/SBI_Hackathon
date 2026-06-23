"""
Chalao agent: guides the customer step-by-step through YONO app interfaces.
"""
from app.agents.state import AgentState
from app.agents.chalao.yono_navigator import YONONavigator

async def chalao_node(state: AgentState) -> AgentState:
    """Prepares navigational steps based on targeted matched schemes."""
    schemes = state.get("matched_schemes", [])
    if schemes:
        navigator = YONONavigator()
        steps = navigator.get_steps(schemes[0])
        state["form_prefilled"] = {
            "navigation_steps": steps,
            "prefilled_fields": {"account_number": "XXXX7823", "kyc_status": "verified"}
        }
    return state
