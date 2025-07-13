"""
Pytest configuration for the Quorum app tests
"""

import os

# Set test environment BEFORE any other imports
os.environ["ENVIRONMENT"] = "test"

import pytest


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
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def sync_session(app):
    """Yield the Flask-SQLAlchemy db.session for use in tests, ensuring all tables are created."""
    from app import db

    with app.app_context():
        yield db.session


@pytest.fixture
def sample_legislator(sync_session):
    """Create a sample legislator for testing."""
    from app.models import Legislator

    legislator = Legislator(id=1, name="John Doe")
    sync_session.add(legislator)
    sync_session.commit()
    return legislator


@pytest.fixture
def sample_bill(sync_session, sample_legislator):
    """Create a sample bill for testing."""
    from app.models import Bill

    bill = Bill(id=1, title="Test Bill", sponsor_id=sample_legislator.id)
    sync_session.add(bill)
    sync_session.commit()
    return bill


@pytest.fixture
def sample_vote(sync_session, sample_bill):
    """Create a sample vote for testing."""
    from app.models import Vote

    vote = Vote(id=1, bill_id=sample_bill.id)
    sync_session.add(vote)
    sync_session.commit()
    return vote


@pytest.fixture
def sample_data(sample_legislator, sample_bill, sample_vote):
    """Fixture that provides all sample data together."""
    return {"legislator": sample_legislator, "bill": sample_bill, "vote": sample_vote}


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sync_session(app):
    """Yield the Flask-SQLAlchemy db.session for use in tests, ensuring all tables are created."""
    from app import db

    with app.app_context():
        yield db.session


@pytest.fixture
def sample_legislator(sync_session):
    """Create a sample legislator for testing."""
    from app.models import Legislator

    legislator = Legislator(id=1, name="John Doe")
    sync_session.add(legislator)
    sync_session.commit()
    return legislator


@pytest.fixture
def sample_bill(sync_session, sample_legislator):
    """Create a sample bill for testing."""
    from app.models import Bill

    bill = Bill(id=1, title="Test Bill", sponsor_id=sample_legislator.id)
    sync_session.add(bill)
    sync_session.commit()
    return bill


@pytest.fixture
def sample_vote(sync_session, sample_bill):
    """Create a sample vote for testing."""
    from app.models import Vote

    vote = Vote(id=1, bill_id=sample_bill.id)
    sync_session.add(vote)
    sync_session.commit()
    return vote


@pytest.fixture
def sample_data(sample_legislator, sample_bill, sample_vote):
    """Fixture that provides all sample data together."""
    return {"legislator": sample_legislator, "bill": sample_bill, "vote": sample_vote}
