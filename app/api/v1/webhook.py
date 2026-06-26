"""
WhatsApp entrypoint endpoints mapping inbound messaging models.
"""
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.schemas.webhook import WebhookPayload, WebhookResponse
from app.services.queue_manager import QueueManager

router = APIRouter()
queue_manager = QueueManager()

@router.post("", response_model=WebhookResponse)
async def inbound_message(request: Request, payload: WebhookPayload, db: AsyncSession = Depends(get_db_session)):
    """Receives and processes incoming messaging API payload."""
    sender = "+919400000000"
    body = "Hello BankSaathi KCC"
    
    # Extract channel from headers (whatsapp, sms, ivr, yono)
    channel = request.headers.get("X-Channel", "whatsapp").lower()
    
    # Try parsing details from WhatsApp Cloud entry layout structure
    if channel == "whatsapp" and payload.entry and len(payload.entry) > 0:
        entry = payload.entry[0]
        changes = entry.get("changes", [])
        if changes and len(changes) > 0:
            value = changes[0].get("value", {})
            messages = value.get("messages", [])
            if messages and len(messages) > 0:
                msg = messages[0]
                sender = msg.get("from", sender)
                body = msg.get("text", {}).get("body", body)
                
    task_payload = {
        "sender": sender,
        "body": body,
        "channel": channel
    }
    
    success = await queue_manager.enqueue_task(task_payload)
    if success:
        return {"status": "accepted", "message": "Payload queued"}
    else:
        return {"status": "error", "message": "Failed to buffer task payload"}


@router.get("")
async def verify_hub(request: Request):
    """Processes verification challenge registration checks from WhatsApp Cloud."""
    challenge = request.query_params.get("hub.challenge", "")
    return Response(content=challenge)

