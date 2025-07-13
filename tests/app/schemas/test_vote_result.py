from datetime import datetime

import pytest

from app.schemas.vote_result import (
    VoteResultCreate,
    VoteResultDetail,
    VoteResultResponse,
)


class TestVoteResultSchemas:
    def test_vote_result_create_valid(self):
        """Test valid vote result creation schema"""
        data = {"legislator_id": 1, "vote_id": 1, "vote_type": 1}
        vote_result = VoteResultCreate(**data)
        assert vote_result.legislator_id == 1
        assert vote_result.vote_id == 1
        assert vote_result.vote_type == 1

    def test_vote_result_create_missing_fields(self):
        """Test vote result creation with missing fields"""
        with pytest.raises(ValueError):
            VoteResultCreate(legislator_id=1)  # Missing vote_id and vote_type

    def test_vote_result_create_invalid_vote_type(self):
        """Test vote result creation with invalid vote type"""
        data = {"legislator_id": 1, "vote_id": 1, "vote_type": 3}  # Invalid vote type
        # This should raise a validation error
        with pytest.raises(ValueError):
            VoteResultCreate(**data)

    def test_vote_result_response_valid(self):
        """Test valid vote result response schema"""
        data = {
            "id": 1,
            "legislator_id": 1,
            "vote_id": 1,
            "vote_type": 1,
            "created_at": datetime.now(),
            "updated_at": None,
        }
        vote_result = VoteResultResponse(**data)
        assert vote_result.id == 1
        assert vote_result.legislator_id == 1
        assert vote_result.vote_id == 1
        assert vote_result.vote_type == 1

    def test_vote_result_detail_valid(self):
        """Test valid vote result detail schema"""
        data = {
            "id": 1,
            "legislator_id": 1,
            "vote_id": 1,
            "vote_type": 1,
            "created_at": datetime.now(),
            "updated_at": None,
            "legislator_name": "John Doe",
            "bill_title": "Test Bill",
            "vote_type_str": "yea",
        }
        vote_result = VoteResultDetail(**data)
        assert vote_result.legislator_name == "John Doe"
        assert vote_result.bill_title == "Test Bill"
        assert vote_result.vote_type_str == "yea"

    def test_vote_type_validation(self):
        """Test vote type validation"""
        # Valid vote types
        VoteResultCreate(legislator_id=1, vote_id=1, vote_type=1)  # yea
        VoteResultCreate(legislator_id=1, vote_id=1, vote_type=2)  # nay

    def test_vote_result_id_validation(self):
        """Test vote result ID field validation"""
        # Negative IDs should be valid
        data = {
            "id": -1,
            "legislator_id": 1,
            "vote_id": 1,
            "vote_type": 1,
            "created_at": datetime.now(),
            "updated_at": None,
        }
        vote_result = VoteResultResponse(**data)
        assert vote_result.id == -1
