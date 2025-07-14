from tests.factories import create_bill, create_legislator


class TestBills:
    def test_list_bills_html(self, client, db_session):
        """Test bills list HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Bill" in response.get_data(as_text=True)

    def test_list_bills_json(self, client, db_session):
        """Test bills list JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert len(data["bills"]) == 1
        assert data["bills"][0]["title"] == "Test Bill"
        assert data["bills"][0]["id"] == bill.id

    def test_list_bills_json_accept_header(self, client, db_session):
        """Test bills list with Accept: application/json header"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills", headers={"Accept": "application/json"})
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert len(data["bills"]) == 1
        assert data["bills"][0]["title"] == "Test Bill"
        assert data["bills"][0]["id"] == bill.id

    def test_list_bills_csv(self, client, db_session):
        """Test bills list CSV endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=bills.csv" in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,title,sponsor_id" in csv_content
        assert f"{bill.id},Test Bill,{legislator.id}" in csv_content

    def test_list_bills_csv_accept_header(self, client, db_session):
        """Test bills list with Accept: text/csv header"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills", headers={"Accept": "text/csv"})
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=bills.csv" in response.headers["Content-Disposition"]
        )
        csv_content = response.get_data(as_text=True)
        assert "id,title,sponsor_id" in csv_content
        assert f"{bill.id},Test Bill,{legislator.id}" in csv_content

    def test_get_bill_json(self, client, db_session):
        """Test single bill JSON endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get(f"/bills/{bill.id}?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert data["bill"]["title"] == "Test Bill"
        assert data["bill"]["id"] == bill.id

    def test_get_bill_json_accept_header(self, client, db_session):
        """Test single bill JSON via Accept header"""
        # Create test data using factories
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get(
            f"/bills/{bill.id}",
            headers={"Accept": "application/json"},
        )
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert data["bill"]["title"] == "Test Bill"
        assert data["bill"]["id"] == bill.id

    def test_get_bill_not_found(self, client):
        """Test bill not found"""
        response = client.get("/bills/999?format=json")
        assert response.status_code == 404
        assert "Not Found" in response.get_data(as_text=True)

    def test_get_bill_html(self, client, db_session):
        """Test single bill HTML endpoint"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get(f"/bills/{bill.id}")
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        assert "Test Bill" in response.get_data(as_text=True)

    def test_invalid_bill_id_format(self, client):
        """Test invalid bill ID format"""
        response = client.get("/bills/invalid")
        assert response.status_code == 404

    def test_list_bills_json_format_param(self, client, db_session):
        """Test bills list with ?format=json parameter"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert len(data["bills"]) == 1
        assert data["bills"][0]["title"] == "Test Bill"

    def test_list_bills_csv_format_param(self, client, db_session):
        """Test bills list with ?format=csv parameter"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get("/bills?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["Content-Type"]
        assert (
            "attachment; filename=bills.csv" in response.headers["Content-Disposition"]
        )

    def test_get_bill_json_format_param(self, client, db_session):
        """Test single bill with ?format=json parameter"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)

        response = client.get(f"/bills/{bill.id}?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        data = response.get_json()
        assert data["bill"]["title"] == "Test Bill"
        assert data["bill"]["id"] == bill.id
