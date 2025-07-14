#!/usr/bin/env python3
"""
Run script for Quorum App
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app

environment = os.environ.get("ENVIRONMENT", "development")
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", "8000"))

if __name__ == "__main__":
    if environment == "production":
        # Disable reloader in production mode
        use_reloader = False
        debug = False
    else:
        # Default to development settings if environment is not recognized
        use_reloader = True
        debug = True

    app = create_app()
    app.run(host=host, port=port, debug=debug, use_reloader=use_reloader)
