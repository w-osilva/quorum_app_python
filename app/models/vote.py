from app import db
from app.models.base import BaseModel


class Vote(BaseModel):
    __tablename__ = "votes"
    bill_id = db.Column(db.Integer, db.ForeignKey("bills.id"))
    bill = db.relationship("Bill", back_populates="votes")
    vote_results = db.relationship("VoteResult", back_populates="vote")

    @property
    def vote_results_count(self):
        """Count of vote results associated with the vote"""
        return len(self.vote_results)

    @property
    def bill_title(self):
        """Title of the bill associated with the vote"""
        return self.bill.title if self.bill else None
