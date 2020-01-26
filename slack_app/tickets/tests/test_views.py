import pytest
from tickets.models import Ticket, Namespace


@pytest.mark.django_db
class TestExperiment(object):

    @pytest.fixture(autouse=True)
    def setup_stuff(self, db):
        namespace = Namespace.objects.create(name='teamwork')
        Ticket.objects.create(title="hahahah", description="asfasfga", status="doing", severity="low", reporter="marzec", namespace=namespace)

    def test_something(self):
        assert Ticket.objects.filter(title="hahahah").exists()
