import pytest

from app import db
from app.models import Bill, Legislator, Vote


@pytest.fixture
def sample_data(app):
    """Create sample data for testing votes routes."""
    with app.app_context():
        legislator = Legislator(id=1, name="Test Legislator")
        db.session.add(legislator)
        bill = Bill(id=1, title="Test Bill", sponsor_id=1)
        db.session.add(bill)
        vote = Vote(id=1, bill_id=1)
        db.session.add(vote)
        db.session.commit()
        yield
        # Cleanup is automatic since we're using in-memory database


class TestVotesAPI:
    def test_list_votes_html(self, client, sample_data):
        response = client.get("/votes")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Bill" in response.get_data(
            as_text=True,
        ) or "votes" in response.get_data(as_text=True)

    def test_list_votes_json(self, client, sample_data):
        response = client.get("/votes?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["votes"]) == 1
        assert data["votes"][0]["bill_id"] == 1
        assert data["votes"][0]["id"] == 1

    def test_list_votes_csv(self, client, sample_data):
        response = client.get("/votes?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=votes.csv" in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,bill_id" in csv_content
        assert "1,1" in csv_content

    def test_get_vote_json(self, client, sample_data):
        response = client.get("/votes/1?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["vote"]["bill_id"] == 1
        assert data["vote"]["id"] == 1

    def test_get_vote_not_found(self, client):
        response = client.get("/votes/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_vote_html(self, client, sample_data):
        response = client.get("/votes/1")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "votes" in response.get_data(as_text=True)

    def test_invalid_vote_id_format(self, client):
        response = client.get("/votes/invalid")
        assert response.status_code == 404
