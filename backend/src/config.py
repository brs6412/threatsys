from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from pathlib import Path
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    database_url: str
    api_host: str
    api_port: int
    environment: str = "development"
    debug: bool = False
    cors_origins: List[AnyHttpUrl] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]

    class Config:
        # Load .env from root (two levels up from config.py)
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        object.__setattr__(self, "debug", self.environment == "development")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
