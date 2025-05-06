# config/settings.py

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "NOMAD Training Navigator 2"
    DATA_DIR: Path = Path("data/metadata")
    LOG_DIR: Path = Path("logs")
    DEFAULT_LANGUAGE: str = "en"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    class Config:
        env_prefix = "NTN_"
        env_file = ".env"


settings = Settings()
