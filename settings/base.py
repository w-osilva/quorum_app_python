import os
from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # Database settings
    database_url: str = "sqlite+aiosqlite:///./data/quorum_app.db"

    # Application settings
    app_name: str = "Quorum App"
    app_version: str = "1.0.0"
    debug: bool = True
    testing: bool = False

    # CORS settings
    allowed_hosts: list = ["*"]

    # CSV import settings
    batch_size: int = 100

    # External services (can be disabled in tests)
    external_api_enabled: bool = True

    # Logging
    log_level: str = "INFO"
