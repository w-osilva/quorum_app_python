from tests.factories import (
    create_legislator,
)


class TestLegislatorsAPI:
    def test_list_legislators_html(self, client, db_session):
        """Test legislators list HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")

        response = client.get("/legislators")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Legislator" in response.get_data(as_text=True)

    def test_list_legislators_json(self, client, db_session):
        """Test legislators list JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")

        response = client.get("/legislators?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["legislators"]) == 1
        assert data["legislators"][0]["name"] == "Test Legislator"
        assert data["legislators"][0]["id"] == legislator.id

    def test_list_legislators_csv(self, client, db_session):
        """Test legislators list CSV endpoint"""
        legislator = create_legislator(name="Test Legislator")

        response = client.get("/legislators?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=legislators.csv"
            in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,name,party" in csv_content
        assert f"{legislator.id},Test Legislator" in csv_content

    def test_get_legislator_json(self, client, db_session):
        """Test single legislator JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")

        response = client.get(f"/legislators/{legislator.id}?format=json")
        assert response.status_code == 200
        data = response.get_json()
        assert data["legislator"]["name"] == "Test Legislator"
        assert data["legislator"]["id"] == legislator.id

    def test_get_legislator_not_found(self, client):
        """Test legislator not found"""
        response = client.get("/legislators/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_legislator_html(self, client, db_session):
        """Test single legislator HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")

        response = client.get(f"/legislators/{legislator.id}")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Legislator" in response.get_data(as_text=True)

    def test_invalid_legislator_id_format(self, client):
        """Test invalid legislator ID format"""
        response = client.get("/legislators/invalid")
        assert response.status_code == 404
