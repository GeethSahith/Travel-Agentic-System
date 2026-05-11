"""
Centralized configuration — reads API keys and settings from .env file.
Only 2 API keys needed: OpenWeatherMap + Serper.dev
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"

    # APIs
    OPENWEATHER_API_KEY: str = ""
    SERPER_API_KEY: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
