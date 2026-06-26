"""
LangGraph shared State type declaration.
"""
from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    customer_id: Optional[str]
    phone_number: str
    messages: List[Dict[str, Any]]
    dms_level: int
    intent: Optional[str]
    language: str
    risk_tier: int
    matched_schemes: List[str]
    form_prefilled: Dict[str, Any]
    requires_officer: bool
    recovery_context: Dict[str, Any]
    profile_score: int
    missing_fields: List[str]
    declarations: Dict[str, Any]
    otp_verified: bool

