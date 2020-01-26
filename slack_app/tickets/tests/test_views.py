import pytest
from tickets.models import Ticket, Namespace


@pytest.mark.django_db
class TestExperiment:

    def test_something(self, tickets):
        assert Namespace.objects.count() == 3
        assert Ticket.objects.count() == 10
