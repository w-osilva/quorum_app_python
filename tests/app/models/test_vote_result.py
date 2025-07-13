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


class TestVoteResult:
    def test_vote_result_creation(self, sync_session, sample_legislator, sample_vote):
        """Test vote result creation"""
        vote_result = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=sample_vote.id,
            vote_type=1,
        )
        sync_session.add(vote_result)
        sync_session.commit()

        assert vote_result.id is not None
        assert vote_result.legislator_id == sample_legislator.id
        assert vote_result.vote_id == sample_vote.id
        assert vote_result.vote_type == 1

    def test_vote_result_vote_type_label(
        self,
        sync_session,
        sample_legislator,
        sample_vote,
    ):
        """Test vote result vote_type_str property"""
        yea_vote = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=sample_vote.id,
            vote_type=1,
        )
        nay_vote = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=sample_vote.id,
            vote_type=2,
        )

        assert yea_vote.vote_type_label == "Yea"
        assert nay_vote.vote_type_label == "Nay"

    def test_vote_result_relationships(
        self,
        sync_session,
        sample_legislator,
        sample_vote,
    ):
        """Test vote result relationships"""
        vote_result = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=sample_vote.id,
            vote_type=1,
        )
        sync_session.add(vote_result)
        sync_session.commit()

        assert vote_result.legislator.id == sample_legislator.id
        assert vote_result.vote.id == sample_vote.id

    def test_vote_result_repr(self, sync_session, sample_legislator, sample_vote):
        """Test vote result string representation"""
        vote_result = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=sample_vote.id,
            vote_type=1,
        )
        assert f"<VoteResult {vote_result.id}>" in str(vote_result)

    def test_vote_result_invalid_vote_type(
        self,
        sync_session,
        sample_legislator,
        sample_vote,
    ):
        """Test vote result with invalid vote type"""
        vote_result = VoteResult(
            legislator_id=sample_legislator.id,
            vote_id=sample_vote.id,
            vote_type=3,  # Invalid vote type
        )

        # Should still work as vote_type is just an integer
        assert vote_result.vote_type is None
        assert vote_result.vote_type_label is None
