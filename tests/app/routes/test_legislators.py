import pytest

from app import db
from app.models import Bill, Legislator, Vote, VoteResult


@pytest.fixture
def sample_data(app):
    """Create sample data for testing legislators routes."""
    with app.app_context():
        # Create sample data for testing
        legislator = Legislator(id=1, name="Test Legislator")
        db.session.add(legislator)
        bill = Bill(id=1, title="Test Bill", sponsor_id=1)
        db.session.add(bill)
        vote = Vote(id=1, bill_id=1)
        db.session.add(vote)
        vote_result = VoteResult(id=1, legislator_id=1, vote_id=1, vote_type=1)
        db.session.add(vote_result)
        db.session.commit()
        yield
        # Cleanup is automatic since we're using in-memory database


class TestLegislatorsAPI:
    def test_list_legislators_html(self, client, sample_data):
        response = client.get("/legislators")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Legislator" in response.get_data(as_text=True)

    def test_list_legislators_json(self, client, sample_data):
        response = client.get("/legislators?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["legislators"]) == 1
        assert data["legislators"][0]["name"] == "Test Legislator"
        assert data["legislators"][0]["id"] == 1

    def test_list_legislators_csv(self, client, sample_data):
        response = client.get("/legislators?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=legislators.csv"
            in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,name,party" in csv_content
        assert "1,Test Legislator" in csv_content

    def test_get_legislator_json(self, client, sample_data):
        response = client.get("/legislators/1?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["legislator"]["name"] == "Test Legislator"
        assert data["legislator"]["id"] == 1

    def test_get_legislator_not_found(self, client):
        response = client.get("/legislators/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_legislator_html(self, client, sample_data):
        response = client.get("/legislators/1")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Legislator" in response.get_data(as_text=True)

    def test_invalid_legislator_id_format(self, client):
        response = client.get("/legislators/invalid")
        assert response.status_code == 404  # Flask returns 404 for invalid int
