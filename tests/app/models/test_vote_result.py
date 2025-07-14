from tests.factories import (
    create_bill,
    create_legislator,
    create_vote,
    create_vote_result,
    create_vote_results,
)


class TestVoteResult:
    def test_vote_result_creation(self, db_session):
        """Test vote result creation"""
        legislator = create_legislator()
        vote = create_vote()
        vote_result = create_vote_result(legislator=legislator, vote=vote)
        assert vote_result.id is not None
        assert vote_result.legislator_id == legislator.id
        assert vote_result.vote_id == vote.id

    def test_vote_result_relationships(self, db_session):
        """Test vote result relationships"""
        legislator = create_legislator()
        vote = create_vote()
        vote_result = create_vote_result(legislator=legislator, vote=vote)
        assert vote_result.legislator is not None
        assert vote_result.legislator.id == legislator.id
        assert vote_result.vote is not None
        assert vote_result.vote.id == vote.id

    def test_vote_result_vote_type(self, db_session):
        """Test vote result vote type"""
        vote_result = create_vote_result()
        assert vote_result.vote_type in [1, 2]

    def test_vote_result_repr(self, db_session):
        """Test vote result string representation"""
        vote_result = create_vote_result()
        assert f"<VoteResult {vote_result.id}>" in str(vote_result)

    def test_vote_result_with_custom_attributes(self, db_session):
        """Test creating vote result with custom attributes"""
        legislator = create_legislator(name="Custom Legislator")
        bill = create_bill(title="Custom Bill")
        vote = create_vote(bill=bill)
        vote_result = create_vote_result(legislator=legislator, vote=vote)
        assert vote_result.legislator.name == "Custom Legislator"
        assert vote_result.vote.bill.title == "Custom Bill"

    def test_multiple_vote_results(self, db_session):
        """Test creating multiple vote results"""
        vote_results = create_vote_results(count=5)
        assert len(vote_results) == 5
        assert all(vote_result.id is not None for vote_result in vote_results)
        assert len(set(vote_result.id for vote_result in vote_results)) == 5
