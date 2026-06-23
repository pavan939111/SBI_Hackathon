"""
Queue Hatao agent: handles appointment schedules and DMS level increments.
"""
from app.agents.state import AgentState
from app.agents.queue_hatao.dms_tracker import DMSTracker

async def queue_hatao_node(state: AgentState) -> AgentState:
    """Resolves scheduling queues and updates digital adoption maturity score."""
    tracker = DMSTracker()
    cust_id = state.get("customer_id")
    if cust_id:
        # Progresses target to level 2
        tracker.update_score(cust_id, 2)
        state["dms_level"] = 2
    return state
