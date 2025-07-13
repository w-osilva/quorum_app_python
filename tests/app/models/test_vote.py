import pytest

from app.models.bill import Bill
from app.models.legislator import Legislator
from app.models.vote import Vote
from app.models.vote_result import VoteResult


@pytest.fixture
def sample_legislator(sync_session):
    """Create a sample legislator for testing"""
    legislator = Legislator(id=1, name="Test Legislator")
    sync_session.add(legislator)
    sync_session.commit()
    return legislator


@pytest.fixture
def sample_bill(sync_session, sample_legislator):
    """Create a sample bill for testing"""
    bill = Bill(id=1, title="Test Bill", sponsor_id=sample_legislator.id)
    sync_session.add(bill)
    sync_session.commit()
    return bill


@pytest.fixture
def sample_vote(sync_session, sample_bill):
    """Create a sample vote for testing"""
    vote = Vote(id=1, bill_id=sample_bill.id)
    sync_session.add(vote)
    sync_session.commit()
    return vote


class TestVote:
    def test_vote_creation(self, sync_session, sample_bill):
        """Test vote creation"""
        vote = Vote(bill_id=sample_bill.id)
        sync_session.add(vote)
        sync_session.commit()

        assert vote.id is not None
        assert vote.bill_id == sample_bill.id

    def test_vote_relationships(self, sync_session, sample_vote, sample_bill):
        """Test vote relationships"""
        assert sample_vote.bill.id == sample_bill.id
        assert sample_vote.bill.title == sample_bill.title

    def test_vote_repr(self, sample_vote):
        """Test vote string representation"""
        assert f"<Vote {sample_vote.id}>" in str(sample_vote)

    def test_vote_vote_results_relationship(self, sync_session, sample_vote):
        """Test vote vote_results relationship"""
        # Create vote results
        vote_result1 = VoteResult(legislator_id=1, vote_id=sample_vote.id, vote_type=1)
        vote_result2 = VoteResult(legislator_id=2, vote_id=sample_vote.id, vote_type=2)
        sync_session.add_all([vote_result1, vote_result2])
        sync_session.commit()

        # Refresh to get updated relationships
        sync_session.refresh(sample_vote)

        assert len(sample_vote.vote_results) == 2
        assert sample_vote.vote_results[0].vote_id == sample_vote.id
        assert sample_vote.vote_results[1].vote_id == sample_vote.id
