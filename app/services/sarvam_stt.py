"""
HTTP client processing transcripts from voice files using Sarvam APIs.
"""
import httpx
from app.core.config import settings

class SarvamSTTService:
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Converts raw audio file bytes to text transcription using Sarvam AI."""
        # TODO: send multipart files payload to Sarvam endpoint
        return "I need a Kisan Credit Card loan"
