import factory
from factory.declarations import SelfAttribute, Sequence, SubFactory
from factory.faker import Faker

from app.models import Bill

from .legislator_factory import LegislatorFactory


class BillFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Bill instances."""

    class Meta:
        model = Bill
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    title = Faker("sentence", nb_words=6)
    sponsor = SubFactory(LegislatorFactory)
    sponsor_id = SelfAttribute("sponsor.id")


def create_bill(**kwargs):
    """Create a single bill with optional overrides."""
    return BillFactory(**kwargs)


def create_bills(count=2, **kwargs):
    """Create multiple bills."""
    return BillFactory.create_batch(count, **kwargs)
