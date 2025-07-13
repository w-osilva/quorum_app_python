from datetime import datetime

import pytest

from app.schemas.vote import VoteCreate, VoteDetail, VoteResponse


class TestVoteSchemas:
    def test_vote_create_valid(self):
        """Test valid vote creation schema"""
        data = {"bill_id": 1}
        vote = VoteCreate(**data)
        assert vote.bill_id == 1

    def test_vote_create_missing_bill_id(self):
        """Test vote creation with missing bill_id"""
        with pytest.raises(ValueError):
            VoteCreate()

    def test_vote_response_valid(self):
        """Test valid vote response schema"""
        data = {"id": 1, "bill_id": 1, "created_at": datetime.now(), "updated_at": None}
        vote = VoteResponse(**data)
        assert vote.id == 1
        assert vote.bill_id == 1

    def test_vote_detail_valid(self):
        """Test valid vote detail schema"""
        data = {
            "id": 1,
            "bill_id": 1,
            "created_at": datetime.now(),
            "updated_at": None,
            "bill_title": "Test Bill",
            "vote_results_count": 10,
        }
        vote = VoteDetail(**data)
        assert vote.bill_title == "Test Bill"
        assert vote.vote_results_count == 10

    def test_vote_bill_id_validation(self):
        """Test vote bill_id validation"""
        # Negative bill_id should be valid
        data = {"bill_id": -1}
        vote = VoteCreate(**data)
        assert vote.bill_id == -1
