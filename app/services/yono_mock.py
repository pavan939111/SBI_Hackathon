"""
Service mapping mock client responses from YONO app server.
"""
import httpx
from app.core.config import settings

class YONOMockClient:
    def __init__(self):
        self.base_url = settings.YONO_MOCK_BASE_URL
        
    async def check_user_profile(self) -> dict:
        """Queries local YONO mock endpoint profile details."""
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(f"{self.base_url}/profile")
                return r.json()
            except Exception:
                return {"customer_id": "MOCK_CUST", "dms_level": 1}
