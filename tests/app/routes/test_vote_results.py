from tests.factories import (
    create_bill,
    create_legislator,
    create_vote,
    create_vote_result,
)


class TestVoteResultsAPI:
    def test_list_vote_results_html(self, client, db_session):
        """Test vote results list HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)
        vote_result = create_vote_result(legislator=legislator, vote=vote)

        response = client.get("/vote_results")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Legislator" in response.get_data(
            as_text=True,
        ) or "vote_results" in response.get_data(as_text=True)

    def test_list_vote_results_json(self, client, db_session):
        """Test vote results list JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)
        vote_result = create_vote_result(legislator=legislator, vote=vote)

        response = client.get("/vote_results?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["vote_results"]) == 1
        assert data["vote_results"][0]["vote_id"] == vote.id
        assert data["vote_results"][0]["id"] == vote_result.id

    def test_list_vote_results_csv(self, client, db_session):
        """Test vote results list CSV endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)
        vote_result = create_vote_result(legislator=legislator, vote=vote)

        response = client.get("/vote_results?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=vote_results.csv"
            in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "vote_id,legislator_id,vote_type" in csv_content
        assert f"{vote.id},{legislator.id},{vote_result.vote_type}" in csv_content

    def test_get_vote_result_json(self, client, db_session):
        """Test single vote result JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)
        vote_result = create_vote_result(legislator=legislator, vote=vote)

        response = client.get(f"/vote_results/{vote_result.id}?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["vote_result"]["vote_id"] == vote.id
        assert data["vote_result"]["id"] == vote_result.id

    def test_get_vote_result_not_found(self, client):
        """Test vote result not found"""
        response = client.get("/vote_results/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_vote_result_html(self, client, db_session):
        """Test single vote result HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)
        vote_result = create_vote_result(legislator=legislator, vote=vote)

        response = client.get(f"/vote_results/{vote_result.id}")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "vote_results" in response.get_data(as_text=True)

    def test_invalid_vote_result_id_format(self, client):
        """Test invalid vote result ID format"""
        response = client.get("/vote_results/invalid")
        assert response.status_code == 404
