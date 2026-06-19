import os
from dotenv import load_dotenv

class Config:
    """Centralized configuration management"""

    def __init__(self):
        load_dotenv() # Load environment variables from .env file
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-for-development")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
        self.DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        self.RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))
        self.RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))
        self.CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", "another-super-secret-key")
        self.MASTER_ENCRYPTION_KEY = os.getenv("MASTER_ENCRYPTION_KEY", "default-encryption-key")
        self.ENCRYPTION_SALT = os.getenv("ENCRYPTION_SALT", "c2FsdHlzYWx0eXNhbHQ=") # base64 encoded "saltysaltysalt"

    def get(self, key: str, default=None):
        """Get a configuration value by key"""
        return getattr(self, key, default)

# Initialize config
settings = Config()
