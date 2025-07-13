import os

from pydantic import ConfigDict

from .base import Settings


class DevelopmentSettings(Settings):
    """Development environment settings"""

    model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # Override base settings for development
    debug: bool = True

    # Development database
    database_url: str = (
        f"sqlite+aiosqlite:///{os.path.abspath('data/quorum_app.development.db')}"
    )

    # Development-specific settings
    reload: bool = True
    log_level: str = "debug"

    # CORS settings for development
    allowed_hosts: list = ["*"]
