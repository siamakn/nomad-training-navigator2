# config/settings.py

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "NOMAD Training Navigator 2"
    DATA_DIR: Path = Path("data/metadata")
    LOG_DIR: Path = Path("logs")
    DEFAULT_LANGUAGE: str = "en"

    class Config:
        env_prefix = "NTN_"  # e.g., NTN_DATA_DIR


settings = Settings()
