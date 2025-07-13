import pytest

from app import db
from app.models import Bill, Legislator, Vote, VoteResult


@pytest.fixture
def sample_data(app):
    """Create sample data for testing vote results routes."""
    with app.app_context():
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


class TestVoteResultsAPI:
    def test_list_vote_results_html(self, client, sample_data):
        response = client.get("/vote_results")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Legislator" in response.get_data(
            as_text=True,
        ) or "vote_results" in response.get_data(as_text=True)

    def test_list_vote_results_json(self, client, sample_data):
        response = client.get("/vote_results?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["vote_results"]) == 1
        assert data["vote_results"][0]["vote_id"] == 1
        assert data["vote_results"][0]["id"] == 1

    def test_list_vote_results_csv(self, client, sample_data):
        response = client.get("/vote_results?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=vote_results.csv"
            in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "vote_id,legislator_id,vote_type" in csv_content
        assert "1,1,1" in csv_content

    def test_get_vote_result_json(self, client, sample_data):
        response = client.get("/vote_results/1?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["vote_result"]["vote_id"] == 1
        assert data["vote_result"]["id"] == 1

    def test_get_vote_result_not_found(self, client):
        response = client.get("/vote_results/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_vote_result_html(self, client, sample_data):
        response = client.get("/vote_results/1")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "vote_results" in response.get_data(as_text=True)

    def test_invalid_vote_result_id_format(self, client):
        response = client.get("/vote_results/invalid")
        assert response.status_code == 404
