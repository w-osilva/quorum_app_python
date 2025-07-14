from tests.factories import (
    create_bill,
    create_bills,
    create_legislator,
    create_vote,
    create_vote_result,
)


class TestBill:
    def test_bill_creation(self, db_session):
        """Test bill creation"""
        legislator = create_legislator(name="Test Legislator")
        bill = create_bill(title="Test Bill", sponsor=legislator)
        assert bill.id is not None
        assert bill.title == "Test Bill"
        assert bill.sponsor_id == legislator.id

    def test_bill_relationships(self, db_session):
        """Test bill relationships"""
        bill = create_bill()
        assert bill.sponsor is not None
        assert bill.sponsor.id == bill.sponsor_id

    def test_bill_vote_results_property(self, db_session):
        """Test bill vote_results property"""
        bill = create_bill()
        vote1 = create_vote(bill=bill)
        vote2 = create_vote(bill=bill)
        create_vote_result(legislator=create_legislator(), vote=vote1)
        create_vote_result(legislator=create_legislator(), vote=vote2)
        db_session.refresh(bill)
        all_vote_results = []
        for vote in bill.votes:
            all_vote_results.extend(vote.vote_results)
        assert len(all_vote_results) == 2

    def test_bill_repr(self, db_session):
        """Test bill string representation"""
        bill = create_bill()
        assert f"<Bill {bill.id}>" in str(bill)

    def test_bill_votes_relationship(self, db_session):
        """Test bill votes relationship"""
        bill = create_bill()
        create_vote(bill=bill)
        create_vote(bill=bill)
        db_session.refresh(bill)
        assert len(bill.votes) == 2
        assert bill.votes[0].bill_id == bill.id
        assert bill.votes[1].bill_id == bill.id

    def test_bill_with_custom_attributes(self, db_session):
        """Test creating bill with custom attributes"""
        bill = create_bill(
            title="Custom Bill Title",
            sponsor=create_legislator(name="Custom Sponsor"),
        )
        assert bill.title == "Custom Bill Title"
        assert bill.sponsor.name == "Custom Sponsor"

    def test_multiple_bills(self, db_session):
        """Test creating multiple bills"""
        bills = create_bills(count=3)
        assert len(bills) == 3
        assert all(bill.id is not None for bill in bills)
        assert len(set(bill.id for bill in bills)) == 3  # All IDs are unique
