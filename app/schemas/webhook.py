"""
Pydantic schemas validating inbound WhatsApp business API payloads.
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class WebhookMessage(BaseModel):
    id: str
    sender: str
    body: Optional[str] = None
    media_url: Optional[str] = None

class WebhookPayload(BaseModel):
    object: str
    entry: List[Dict[str, Any]]

class WebhookResponse(BaseModel):
    status: str
    message: str
