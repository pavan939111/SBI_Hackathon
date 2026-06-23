"""
Project-wide settings declaration backed by pydantic-settings.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "your_secret_key_here"
    APP_PORT: int = 8000
    DEBUG: bool = True
    
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/banksaathi"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    WHATSAPP_TOKEN: str = "your_whatsapp_token_here"
    WHATSAPP_PHONE_NUMBER_ID: str = "your_phone_number_id_here"
    WHATSAPP_VERIFY_TOKEN: str = "your_verify_token_here"
    
    SARVAM_API_KEY: str = "your_sarvam_api_key_here"
    SARVAM_STT_ENDPOINT: str = "https://api.sarvam.ai/speech-to-text"
    SARVAM_TTS_ENDPOINT: str = "https://api.sarvam.ai/text-to-speech"
    
    GEMINI_API_KEY: str = "your_gemini_api_key_here"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8001
    
    LANGGRAPH_CHECKPOINT_DB: str = "postgresql+psycopg://user:password@localhost:5432/banksaathi"
    
    YONO_MOCK_BASE_URL: str = "http://localhost:8002"
    YONO_MOCK_ENABLED: bool = True
    
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
