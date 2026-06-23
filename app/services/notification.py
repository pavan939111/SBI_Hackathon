"""
Proactive scheduling hooks queuing alerts for Queue Hatao logic.
"""
import logging
from app.services.whatsapp import WhatsAppService

class NotificationService:
    def __init__(self):
        self.wa_service = WhatsAppService()
        
    async def dispatch_nudge(self, phone: str, message: str) -> None:
        """Sends targeted alert to WhatsApp contact."""
        logging.info(f"Dispatching campaign nudge to {phone}")
        await self.wa_service.send_whatsapp_message(phone, message)
