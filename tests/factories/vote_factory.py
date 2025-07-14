import factory
from factory.declarations import SelfAttribute, Sequence, SubFactory

from app.models import Vote

from .bill_factory import BillFactory


class VoteFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Vote instances."""

    class Meta:
        model = Vote
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    bill = SubFactory(BillFactory)
    bill_id = SelfAttribute("bill.id")


def create_vote(**kwargs):
    """Create a single vote with optional overrides."""
    return VoteFactory(**kwargs)


def create_votes(count=1, **kwargs):
    """Create multiple votes."""
    return VoteFactory.create_batch(count, **kwargs)
