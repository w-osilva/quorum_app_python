from tests.factories import (
    create_bill,
    create_legislator,
    create_vote,
    create_vote_result,
    create_votes,
)


class TestVote:
    def test_vote_creation(self, db_session):
        """Test vote creation"""
        bill = create_bill()
        vote = create_vote(bill=bill)
        assert vote.id is not None
        assert vote.bill_id == bill.id

    def test_vote_relationships(self, db_session):
        """Test vote relationships"""
        bill = create_bill()
        vote = create_vote(bill=bill)
        assert vote.bill is not None
        assert vote.bill.id == bill.id

    def test_vote_vote_results(self, db_session):
        """Test vote vote results"""
        vote = create_vote()
        vote_result1 = create_vote_result(vote=vote, legislator=create_legislator())
        vote_result2 = create_vote_result(vote=vote, legislator=create_legislator())
        db_session.refresh(vote)
        assert len(vote.vote_results) == 2
        assert vote_result1.vote_id == vote.id
        assert vote_result2.vote_id == vote.id

    def test_vote_repr(self, db_session):
        """Test vote string representation"""
        vote = create_vote()
        assert f"<Vote {vote.id}>" in str(vote)

    def test_vote_with_custom_attributes(self, db_session):
        """Test creating vote with custom attributes"""
        bill = create_bill(title="Custom Bill")
        vote = create_vote(bill=bill)
        assert vote.bill.title == "Custom Bill"

    def test_multiple_votes(self, db_session):
        """Test creating multiple votes"""
        votes = create_votes(count=3)
        assert len(votes) == 3
        assert all(vote.id is not None for vote in votes)
        assert len(set(vote.id for vote in votes)) == 3
