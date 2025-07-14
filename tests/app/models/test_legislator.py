from tests.factories import (
    create_bill,
    create_legislator,
    create_legislators,
    create_vote,
    create_vote_result,
)


class TestLegislator:
    def test_legislator_creation(self, db_session):
        """Test legislator creation"""
        legislator = create_legislator(name="Test Legislator")
        assert legislator.id is not None
        assert legislator.name == "Test Legislator"

    def test_legislator_relationships(self, db_session):
        """Test legislator relationships"""
        legislator = create_legislator()
        bill = create_bill(sponsor=legislator)
        assert bill.sponsor is not None
        assert bill.sponsor.id == legislator.id

    def test_legislator_vote_results(self, db_session):
        """Test legislator vote results"""
        legislator = create_legislator()
        bill = create_bill(sponsor=create_legislator())
        vote = create_vote(bill=bill)
        vote_result1 = create_vote_result(legislator=legislator, vote=vote)
        vote_result2 = create_vote_result(legislator=legislator, vote=vote)
        db_session.refresh(legislator)
        assert len(legislator.vote_results) == 2
        assert vote_result1.legislator_id == legislator.id
        assert vote_result2.legislator_id == legislator.id

    def test_legislator_repr(self, db_session):
        """Test legislator string representation"""
        legislator = create_legislator()
        assert f"<Legislator {legislator.id}>" in str(legislator)

    def test_legislator_with_custom_attributes(self, db_session):
        """Test creating legislator with custom attributes"""
        legislator = create_legislator(name="Custom Legislator Name")
        assert legislator.name == "Custom Legislator Name"

    def test_multiple_legislators(self, db_session):
        """Test creating multiple legislators"""
        legislators = create_legislators(count=3)
        assert len(legislators) == 3
        assert all(legislator.id is not None for legislator in legislators)
        assert len(set(legislator.id for legislator in legislators)) == 3
