from tests.factories import create_bill, create_legislator, create_vote


class TestVotesAPI:
    def test_list_votes_html(self, client, db_session):
        """Test votes list HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        _vote = create_vote(bill=bill)

        response = client.get("/votes")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Bill" in response.get_data(
            as_text=True,
        ) or "votes" in response.get_data(as_text=True)

    def test_list_votes_json(self, client, db_session):
        """Test votes list JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)

        response = client.get("/votes?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["votes"]) == 1
        assert data["votes"][0]["bill_id"] == bill.id
        assert data["votes"][0]["id"] == vote.id

    def test_list_votes_csv(self, client, db_session):
        """Test votes list CSV endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)

        response = client.get("/votes?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=votes.csv" in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,bill_id" in csv_content
        assert f"{vote.id},{bill.id}" in csv_content

    def test_get_vote_json(self, client, db_session):
        """Test single vote JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)

        response = client.get(f"/votes/{vote.id}?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["vote"]["bill_id"] == bill.id
        assert data["vote"]["id"] == vote.id

    def test_get_vote_not_found(self, client):
        """Test vote not found"""
        response = client.get("/votes/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_vote_html(self, client, db_session):
        """Test single vote HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        vote = create_vote(bill=bill)

        response = client.get(f"/votes/{vote.id}")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "votes" in response.get_data(as_text=True)

    def test_invalid_vote_id_format(self, client):
        """Test invalid vote ID format"""
        response = client.get("/votes/invalid")
        assert response.status_code == 404
