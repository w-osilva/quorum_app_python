from app import db
from app.models.base import BaseModel


class Bill(BaseModel):
    __tablename__ = "bills"
    title = db.Column(db.String, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("legislators.id"))

    # belongs to
    sponsor = db.relationship("Legislator", back_populates="sponsored_bills")

    # Has many
    votes = db.relationship("Vote", back_populates="bill")

    @property
    def votes_count(self):
        """Count of votes associated with the bill"""
        return len(self.votes)

    @property
    def is_supported(self):
        """Check if the bill is supported by the sponsor"""
        return any(vote.is_supported for vote in self.votes)

    @property
    def is_opposed(self):
        """Check if the bill is opposed by the sponsor"""
        return any(vote.is_opposed for vote in self.votes)

    @property
    def vote_results_count(self):
        """Count of vote results associated with the bill"""
        return sum(len(vote.vote_results) for vote in self.votes)
