import pytest
from tickets.models import Ticket, Namespace


@pytest.mark.django_db
class TestExperiment:

    @pytest.fixture(autouse=True)
    def setup_stuff(self, db):

        for name in ['teamwork', 'singlework', 'multiwork']:
            Namespace.objects.create(name=name)

        qs = [
            {
                'title': 'ticket_1',
                'description': 'some description',
                'status': 'doing',
                'severity': 'low',
                'namespace_id': 1,
                'reporter': 'k.marzec',
                'data': {
                    'channels': 'controlling',
                    'workspace': 'finance'
                }
            }
        ]

        for ticket_data in qs:
            Ticket.objects.create(**ticket_data)


    def test_something(self):
        assert Namespace.objects.count() == 3
        assert Ticket.objects.count() == 1
