import pytest

from app import db
from app.models import Bill, Legislator


@pytest.fixture
def sample_data(app):
    """Create sample data for testing bills routes."""
    with app.app_context():
        legislator = Legislator(id=1, name="Test Legislator")
        db.session.add(legislator)
        bill = Bill(id=1, title="Test Bill", sponsor_id=1)
        db.session.add(bill)
        db.session.commit()
        yield
        # Cleanup is automatic since we're using in-memory database


class TestBills:
    def test_list_bills_html(self, client, sample_data):
        response = client.get("/bills")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Bill" in response.get_data(as_text=True)

    def test_list_bills_json(self, client, sample_data):
        response = client.get("/bills?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert len(data["bills"]) == 1
        assert data["bills"][0]["title"] == "Test Bill"
        assert data["bills"][0]["id"] == 1

    def test_list_bills_json_accept_header(self, client, sample_data):
        """Test bills list with Accept: application/json header"""
        response = client.get("/bills", headers={"Accept": "application/json"})
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert len(data["bills"]) == 1
        assert data["bills"][0]["title"] == "Test Bill"
        assert data["bills"][0]["id"] == 1

    def test_list_bills_csv(self, client, sample_data):
        response = client.get("/bills?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=bills.csv" in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,title,sponsor_id" in csv_content
        assert "1,Test Bill,1" in csv_content

    def test_list_bills_csv_accept_header(self, client, sample_data):
        """Test bills list with Accept: text/csv header"""
        response = client.get("/bills", headers={"Accept": "text/csv"})
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=bills.csv" in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,title,sponsor_id" in csv_content
        assert "1,Test Bill,1" in csv_content

    def test_get_bill_json(self, client, sample_data):
        response = client.get("/bills/1?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert data["bill"]["title"] == "Test Bill"
        assert data["bill"]["id"] == 1

    def test_get_bill_json_accept_header(self, client, sample_data):
        """Test single bill JSON via Accept header"""
        response = client.get("/bills/1", headers={"Accept": "application/json"})
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert data["bill"]["title"] == "Test Bill"
        assert data["bill"]["id"] == 1

    def test_get_bill_not_found(self, client):
        response = client.get("/bills/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_bill_html(self, client, sample_data):
        response = client.get("/bills/1")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Bill" in response.get_data(as_text=True)

    def test_invalid_bill_id_format(self, client):
        response = client.get("/bills/invalid")
        assert response.status_code == 404

    def test_list_bills_json_format_param(self, client, sample_data):
        """Test bills list with ?format=json parameter"""
        response = client.get("/bills?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert len(data["bills"]) == 1
        assert data["bills"][0]["title"] == "Test Bill"

    def test_list_bills_csv_format_param(self, client, sample_data):
        """Test bills list with ?format=csv parameter"""
        response = client.get("/bills?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=bills.csv" in response.headers["Content-Disposition"]
        )

    def test_get_bill_json_format_param(self, client, sample_data):
        """Test single bill with ?format=json parameter"""
        response = client.get("/bills/1?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert data["bill"]["title"] == "Test Bill"
        assert data["bill"]["id"] == 1
