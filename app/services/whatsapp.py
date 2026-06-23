"""
HTTP client dispatching messaging objects out to WhatsApp Business Cloud.
"""
import httpx
from app.core.config import settings

class WhatsAppService:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.endpoint = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        
    async def send_whatsapp_message(self, recipient: str, text: str) -> None:
        """Sends WhatsApp text body to targeted recipient."""
        headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"body": text}
        }
        # Safely wrap endpoint delivery for mock/live configurations
        if settings.WHATSAPP_TOKEN != "your_whatsapp_token_here":
            await self.client.post(self.endpoint, json=payload, headers=headers)
