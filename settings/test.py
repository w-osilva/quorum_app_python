import os

from pydantic import ConfigDict

from .base import Settings


class TestSettings(Settings):
    """Test environment settings"""

    model_config = ConfigDict(
        env_file=".env.test",
        case_sensitive=False,
        extra="ignore",
    )

    # Override base settings for test
    debug: bool = True
    testing: bool = True

    # Test database - use in-memory SQLite for fast tests
    database_url: str = "sqlite:///:memory:"

    # Test-specific settings
    reload: bool = False  # Don't reload in tests
    log_level: str = "ERROR"  # Minimal logging during tests

    # CORS settings for test
    allowed_hosts: list = ["*"]

    # Disable external services in tests
    external_api_enabled: bool = False
