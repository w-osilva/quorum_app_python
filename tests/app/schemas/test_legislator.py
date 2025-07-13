from datetime import datetime

import pytest

from app.schemas.legislator import (
    LegislatorCreate,
    LegislatorDetail,
    LegislatorResponse,
)


class TestLegislatorSchemas:
    def test_legislator_create_valid(self):
        """Test valid legislator creation schema"""
        data = {"name": "John Doe"}
        legislator = LegislatorCreate(**data)
        assert legislator.name == "John Doe"

    def test_legislator_create_missing_name(self):
        """Test legislator creation with missing name"""
        with pytest.raises(ValueError):
            LegislatorCreate()

    def test_legislator_response_valid(self):
        """Test valid legislator response schema"""
        data = {
            "id": 1,
            "name": "John Doe",
            "created_at": datetime.now(),
            "updated_at": None,
        }
        legislator = LegislatorResponse(**data)
        assert legislator.id == 1
        assert legislator.name == "John Doe"
        assert legislator.created_at is not None

    def test_legislator_detail_valid(self):
        """Test valid legislator detail schema"""
        data = {
            "id": 1,
            "name": "John Doe",
            "created_at": datetime.now(),
            "updated_at": None,
            "sponsored_bills_count": 5,
            "supported_bills_count": 10,
            "opposed_bills_count": 3,
        }
        legislator = LegislatorDetail(**data)
        assert legislator.sponsored_bills_count == 5
        assert legislator.supported_bills_count == 10
        assert legislator.opposed_bills_count == 3

    def test_legislator_name_validation(self):
        """Test legislator name validation"""
        # Empty name should raise error
        with pytest.raises(ValueError):
            LegislatorCreate(name="")

        # Whitespace-only name should raise error
        with pytest.raises(ValueError):
            LegislatorCreate(name="   ")

    def test_legislator_id_validation(self):
        """Test legislator ID field validation"""
        # Negative IDs should be valid (just integers)
        data = {
            "id": -1,
            "name": "Test",
            "created_at": datetime.now(),
            "updated_at": None,
        }
        legislator = LegislatorResponse(**data)
        assert legislator.id == -1
