"""
Pytest configuration for the Quorum app tests
"""

import importlib
import os
import pkgutil

import pytest

# Set test environment BEFORE any other imports
os.environ["ENVIRONMENT"] = "test"


def setup_factory_sessions(session):
    """Set up factory sessions for testing."""
    # Import factories dynamically and set their sessions
    for _, module_name, _ in pkgutil.iter_modules(["tests/factories"]):
        if module_name != "__init__":
            module = importlib.import_module(f"tests.factories.{module_name}")

            # Find factory classes in the module and set their sessions
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, "_meta") and hasattr(attr._meta, "sqlalchemy_session"):
                    # This is a factory class, set its session
                    attr._meta.sqlalchemy_session = session


@pytest.fixture
def app():
    """Create and configure a new app instance for each test using test settings."""
    # Import only when needed to avoid loading issues
    from app import create_app, db
    from settings import settings

    # Verify we're using test settings
    assert settings.__class__.__name__ == "TestSettings", (
        f"Expected TestSettings, got {settings.__class__.__name__}"
    )

    app = create_app()
    app.config["TESTING"] = True

    # The app should already be using the test database URL from settings
    # Let's verify it's using the right database
    expected_db_url = "sqlite:///:memory:"
    actual_db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    assert expected_db_url in actual_db_url, (
        f"Expected {expected_db_url}, got {actual_db_url}"
    )

    with app.app_context():
        db.create_all()
        yield app
        # Properly close all connections
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """Yield the Flask-SQLAlchemy db.session for use in tests, ensuring proper cleanup."""
    from app import db

    with app.app_context():
        # Create a new session for each test
        session = db.session()

        # Set up factory sessions
        setup_factory_sessions(session)

        try:
            yield session
        finally:
            # Properly close the session and remove it
            session.close()
            db.session.remove()
