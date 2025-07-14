import factory
from factory.declarations import SelfAttribute, Sequence, SubFactory
from factory.faker import Faker

from app.models import VoteResult

from .legislator_factory import LegislatorFactory
from .vote_factory import VoteFactory


class VoteResultFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating VoteResult instances."""

    class Meta:
        model = VoteResult
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    vote = SubFactory(VoteFactory)
    vote_id = SelfAttribute("vote.id")
    legislator = SubFactory(LegislatorFactory)
    legislator_id = SelfAttribute("legislator.id")
    _vote_type = Faker("random_element", elements=[1, 2])  # 1=Yea, 2=Nay


def create_vote_result(**kwargs):
    """Create a single vote result with optional overrides."""
    return VoteResultFactory(**kwargs)


def create_vote_results(count=5, **kwargs):
    """Create multiple vote results."""
    return VoteResultFactory.create_batch(count, **kwargs)
