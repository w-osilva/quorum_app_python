from app import db
from app.constants.vote_type import VoteType
from app.models.base import BaseModel


class VoteResult(BaseModel):
    __tablename__ = "vote_results"
    vote_id = db.Column(db.Integer, db.ForeignKey("votes.id"))
    legislator_id = db.Column(db.Integer, db.ForeignKey("legislators.id"))
    _vote_type = db.Column("vote_type", db.Integer)  # 1=Yea, 2=Nay
    vote = db.relationship("Vote", back_populates="vote_results")
    legislator = db.relationship("Legislator", back_populates="vote_results")

    @property
    def vote_type(self):
        """Get the vote type, returning None if invalid"""
        if self._vote_type in [VoteType.YEA, VoteType.NAY]:
            return self._vote_type
        return None

    @vote_type.setter
    def vote_type(self, value) -> None:
        """Set the vote type, validating it's a valid VoteType"""
        if value in [VoteType.YEA, VoteType.NAY]:
            self._vote_type = value
        else:
            self._vote_type = None  # Set to None if invalid

    @property
    def is_yea(self):
        """Check if the vote result is a 'Yea' vote"""
        return self.vote_type == VoteType.YEA

    @property
    def is_nay(self):
        """Check if the vote result is a 'Nay' vote"""
        return self.vote_type == VoteType.NAY

    @property
    def vote_type_label(self):
        """Return the string representation of the vote type"""
        if self.vote_type is None:
            return None
        try:
            return VoteType.label(self.vote_type)
        except Exception:
            return None
