import os

from .base import Settings
from .development import DevelopmentSettings
from .production import ProductionSettings
from .test import TestSettings

# Get environment from environment variable
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Export the appropriate settings class
if ENVIRONMENT == "production":
    settings = ProductionSettings()
elif ENVIRONMENT == "test":
    settings = TestSettings()
else:
    settings = DevelopmentSettings()

__all__ = [
    "DevelopmentSettings",
    "ProductionSettings",
    "Settings",
    "TestSettings",
    "settings",
]
