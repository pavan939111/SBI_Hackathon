"""
Suraksha agent: handles anomaly flags, block verification, and compliance tiers.
"""
from app.agents.state import AgentState
from app.agents.suraksha.anomaly_detector import AnomalyDetector

async def suraksha_node(state: AgentState) -> AgentState:
    """Scans operations for fraud indicators and executes security gating rules."""
    detector = AnomalyDetector()
    if detector.scan_activity():
        state["risk_tier"] = 3
        state["requires_officer"] = True
    return state
