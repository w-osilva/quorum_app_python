from app import db
from app.models.base import BaseModel


class Legislator(BaseModel):
    __tablename__ = "legislators"
    name = db.Column(db.String, nullable=False)
    party = db.Column(db.String)
    sponsored_bills = db.relationship("Bill", back_populates="sponsor")
    vote_results = db.relationship("VoteResult", back_populates="legislator")

    @property
    def sponsored_bills_count(self):
        """Count of bills sponsored by the legislator"""
        return len(self.sponsored_bills)

    @property
    def supported_bills_count(self):
        """Count of bills supported by the legislator (vote_type=1)"""
        return sum(1 for vote_result in self.vote_results if vote_result.vote_type == 1)

    @property
    def opposed_bills_count(self):
        """Count of bills opposed by the legislator (vote_type=2)"""
        return sum(1 for vote_result in self.vote_results if vote_result.vote_type == 2)
