"""
Configuration settings for Ama Arogya ChatBot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{BASE_DIR}/health_chatbot.db")

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Rasa configuration
RASA_API_URL = os.getenv("RASA_API_URL", "http://localhost:5005")
RASA_ENABLED = os.getenv("RASA_ENABLED", "False").lower() == "true"

# Frontend configuration
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = BASE_DIR / "static"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", f"{BASE_DIR}/logs/app.log")

# Performance settings
MAX_RESPONSE_LENGTH = int(os.getenv("MAX_RESPONSE_LENGTH", 1000))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", 100))

# Supported languages
SUPPORTED_LANGUAGES = ["en", "hi", "or"]
DEFAULT_LANGUAGE = "en"

# Health content cache settings
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # 1 hour
