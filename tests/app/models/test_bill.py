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


class TestBill:
    def test_bill_creation(self, sync_session, sample_legislator):
        """Test bill creation"""
        bill = Bill(title="Test Bill", sponsor_id=sample_legislator.id)
        sync_session.add(bill)
        sync_session.commit()

        assert bill.id is not None
        assert bill.title == "Test Bill"
        assert bill.sponsor_id == sample_legislator.id

    def test_bill_relationships(self, sync_session, sample_bill, sample_legislator):
        """Test bill relationships"""
        # Test sponsor relationship
        assert sample_bill.sponsor.id == sample_legislator.id
        assert sample_bill.sponsor.name == sample_legislator.name

    def test_bill_vote_results_property(self, sync_session, sample_bill):
        """Test bill vote_results property"""
        # Create votes and vote results
        vote1 = Vote(bill_id=sample_bill.id)
        vote2 = Vote(bill_id=sample_bill.id)
        sync_session.add_all([vote1, vote2])
        sync_session.commit()

        # Add vote results
        vote_result1 = VoteResult(legislator_id=1, vote_id=vote1.id, vote_type=1)
        vote_result2 = VoteResult(legislator_id=2, vote_id=vote2.id, vote_type=2)
        sync_session.add_all([vote_result1, vote_result2])
        sync_session.commit()

        # Refresh to get updated relationships
        sync_session.refresh(sample_bill)

        # Access vote results through votes
        all_vote_results = []
        for vote in sample_bill.votes:
            all_vote_results.extend(vote.vote_results)

        assert len(all_vote_results) == 2

    def test_bill_repr(self, sample_bill):
        """Test bill string representation"""
        assert f"<Bill {sample_bill.id}>" in str(sample_bill)

    def test_bill_votes_relationship(self, sync_session, sample_bill):
        """Test bill votes relationship"""
        # Create votes
        vote1 = Vote(bill_id=sample_bill.id)
        vote2 = Vote(bill_id=sample_bill.id)
        sync_session.add_all([vote1, vote2])
        sync_session.commit()

        # Refresh to get updated relationships
        sync_session.refresh(sample_bill)

        assert len(sample_bill.votes) == 2
        assert sample_bill.votes[0].bill_id == sample_bill.id
        assert sample_bill.votes[1].bill_id == sample_bill.id
