from pydantic import ConfigDict

from .base import Settings


class ProductionSettings(Settings):
    """Production environment settings"""

    model_config = ConfigDict(
        env_file=".env.production",
        case_sensitive=False,
        extra="ignore",
    )

    # Override base settings for production
    debug: bool = False

    # Production database (example - would be set via environment variables)
    database_url: str = "postgresql://user:password@localhost/quorum_prod"

    # Production-specific settings
    reload: bool = False
    log_level: str = "info"

    # CORS settings for production
    allowed_hosts: list = ["quorum-app.com", "www.quorum-app.com"]
