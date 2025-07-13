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


class TestLegislator:
    def test_legislator_creation(self, sync_session):
        """Test legislator creation"""
        legislator = Legislator(name="John Doe")
        sync_session.add(legislator)
        sync_session.commit()

        assert legislator.id is not None
        assert legislator.name == "John Doe"
        assert legislator.created_at is not None

    def test_legislator_relationships(self, sync_session, sample_legislator):
        """Test legislator relationships"""
        # Create a bill sponsored by this legislator
        bill = Bill(id=1, title="Test Bill", sponsor_id=sample_legislator.id)
        sync_session.add(bill)
        sync_session.commit()

        # Test sponsored bills relationship
        assert len(sample_legislator.sponsored_bills) == 1
        assert sample_legislator.sponsored_bills[0].id == bill.id

    def test_legislator_vote_counts(self, sync_session, sample_legislator):
        """Test legislator vote count properties"""
        # Create a bill and vote
        bill = Bill(id=1, title="Test Bill", sponsor_id=sample_legislator.id)
        vote = Vote(bill_id=bill.id)
        sync_session.add_all([bill, vote])
        sync_session.commit()

        # Add vote results
        yea_vote = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=vote.id,
            vote_type=1,  # yea
        )
        nay_vote = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=vote.id,
            vote_type=2,  # nay
        )
        sync_session.add_all([yea_vote, nay_vote])
        sync_session.commit()

        # Refresh to get updated relationships
        sync_session.refresh(sample_legislator)

        assert sample_legislator.supported_bills_count == 1
        assert sample_legislator.opposed_bills_count == 1

    def test_legislator_repr(self, sample_legislator):
        """Test legislator string representation"""
        assert f"<Legislator {sample_legislator.id}>" in str(sample_legislator)

    def test_legislator_vote_results_relationship(
        self,
        sync_session,
        sample_legislator,
    ):
        """Test legislator vote results relationship"""
        # Create vote result
        vote_result = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=1,
            vote_type=1,
        )
        sync_session.add(vote_result)
        sync_session.commit()

        # Refresh to get updated relationships
        sync_session.refresh(sample_legislator)

        assert len(sample_legislator.vote_results) == 1
        assert sample_legislator.vote_results[0].vote_type == 1
