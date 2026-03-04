"""Application configuration."""

import os


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", "5000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-change-me")
    JWT_EXPIRY_HOURS = 24
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
