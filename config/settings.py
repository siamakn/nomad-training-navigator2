# config/settings.py

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Global application settings."""

    APP_NAME: str = "NOMAD Training Navigator 2"
    DATA_DIR: Path = Path("data/metadata")
    LOG_DIR: Path = Path("logs")
    DEFAULT_LANGUAGE: str = "en"

    class Config:
        env_prefix = "NTN_"


settings = Settings()
