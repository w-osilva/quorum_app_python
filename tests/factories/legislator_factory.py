import factory
from factory.declarations import Sequence
from factory.faker import Faker

from app.models import Legislator


class LegislatorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Legislator instances."""

    class Meta:
        model = Legislator
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    name = Faker("name")


def create_legislator(**kwargs):
    """Create a single legislator with optional overrides."""
    return LegislatorFactory(**kwargs)


def create_legislators(count=3, **kwargs):
    """Create multiple legislators."""
    return LegislatorFactory.create_batch(count, **kwargs)
