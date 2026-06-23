"""
Pydantic model representing state checkpoint data mappings.
"""
from pydantic import BaseModel
from typing import Dict, Any, List

class AgentStateSchema(BaseModel):
    customer_id: str
    thread_id: str
    current_state: Dict[str, Any]
    history: List[Dict[str, Any]]
