from datetime import datetime

import pytest

from app.schemas.bill import BillCreate, BillDetail, BillResponse


class TestBillSchemas:
    def test_bill_create_valid(self):
        """Test valid bill creation schema"""
        data = {"title": "Test Bill", "sponsor_id": 1}
        bill = BillCreate(**data)
        assert bill.title == "Test Bill"
        assert bill.sponsor_id == 1

    def test_bill_create_missing_fields(self):
        """Test bill creation with missing fields"""
        with pytest.raises(ValueError):
            BillCreate(title="Test Bill")  # Missing sponsor_id

    def test_bill_response_valid(self):
        """Test valid bill response schema"""
        data = {
            "id": 1,
            "title": "Test Bill",
            "sponsor_id": 1,
            "created_at": datetime.now(),
            "updated_at": None,
        }
        bill = BillResponse(**data)
        assert bill.id == 1
        assert bill.title == "Test Bill"
        assert bill.sponsor_id == 1

    def test_bill_detail_valid(self):
        """Test valid bill detail schema"""
        data = {
            "id": 1,
            "title": "Test Bill",
            "sponsor_id": 1,
            "created_at": datetime.now(),
            "updated_at": None,
            "sponsor_name": "John Doe",
            "votes_count": 5,
        }
        bill = BillDetail(**data)
        assert bill.sponsor_name == "John Doe"
        assert bill.votes_count == 5

    def test_bill_title_validation(self):
        """Test bill title validation"""
        # Empty title should raise error
        with pytest.raises(ValueError):
            BillCreate(title="", sponsor_id=1)

    def test_bill_sponsor_id_validation(self):
        """Test bill sponsor_id validation"""
        # Negative sponsor_id should be valid
        data = {"title": "Test Bill", "sponsor_id": -1}
        bill = BillCreate(**data)
        assert bill.sponsor_id == -1
