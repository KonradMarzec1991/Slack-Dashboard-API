import pytest
from tickets.models import (
    Namespace,
    Ticket
)


@pytest.mark.django_db
def test_namespace_model(namespaces):
    for namespace in Namespace.objects.all():
        assert str(namespace) == namespace.name


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('tickets')
class TestTicketsModel:

    def test_str_method(self):
        for ticket in Ticket.objects.all():
            assert str(ticket) == f'{ticket.title} of {ticket.reporter}'

    def test_get_one_column_data(self):
        reporters = Ticket.objects.get_one_column_data('reporter')[:3]
        assert list(reporters) == ['a.olech', 'a.olech', 'k.marzec']

    def test_get_workspace_hierarchy(self):
        workspaces = Ticket.objects.get_workspace_hierarchy()
        assert workspaces == \
               {'hr': ['payments'], 'finance': ['accountancy', 'controlling'],
                'logistics': ['consumer_service', 'product_forecasting']}

