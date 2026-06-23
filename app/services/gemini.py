"""
Inference wrapper client invoking Gemini 1.5 Flash models.
"""
from app.core.config import settings
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
    async def get_chat_response(self, prompt: str) -> str:
        """Calls Gemini API for text processing."""
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
            return "Mocked Gemini Response: OK"
        response = self.model.generate_content(prompt)
        return response.text
