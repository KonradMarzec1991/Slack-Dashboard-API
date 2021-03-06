import pytest

from tickets.models import (
    Ticket,
    Namespace
)


@pytest.fixture
def namespaces():
    for name in ['teamwork', 'singlework', 'multiwork']:
        Namespace.objects.create(name=name)


@pytest.fixture
def tickets(namespaces):
    for ticket_data in qs:
        Ticket.objects.create(**ticket_data)


qs = [
    {
        'title': 'ticket_1',
        'description': 'some description',
        'status': 'doing',
        'severity': 'low',
        'namespace_id': 1,
        'reporter': 'k.marzec',
        'data': {
            'channel': 'controlling',
            'workspace': 'finance'
        }
    },
    {
        'title': 'ticket_2',
        'description': 'some stuff',
        'status': 'done',
        'severity': 'high',
        'namespace_id': 1,
        'reporter': 'a.olech',
        'data': {
            'channel': 'accountancy',
            'workspace': 'finance'
        }
    },
    {
        'title': 'ticket_3',
        'description': 'some other stuff',
        'status': 'done',
        'severity': 'medium',
        'namespace_id': 2,
        'reporter': 'k.marzec',
        'data': {
            'channel': 'controlling',
            'workspace': 'finance'
        }
    },
    {
        'title': 'ticket_4',
        'description': 'some description',
        'status': 'not started',
        'severity': 'low',
        'namespace_id': 1,
        'reporter': 'a.olech',
        'data': {
            'channel': 'consumer_service',
            'workspace': 'logistics'
        }
    },
    {
        'title': 'ticket_5',
        'description': 'some desc',
        'status': 'done',
        'severity': 'medium',
        'namespace_id': 1,
        'reporter': 'k.marzec',
        'data': {
            'channel': 'product_forecasting',
            'workspace': 'logistics'
        }
    },
    {
        'title': 'ticket_6',
        'description': 'some description',
        'status': 'not started',
        'severity': 'high',
        'namespace_id': 2,
        'reporter': 'a.olech',
        'data': {
            'channel': 'consumer_service',
            'workspace': 'logistics'
        }
    },
    {
        'title': 'ticket_7',
        'description': 'some description',
        'status': 'done',
        'severity': 'high',
        'namespace_id': 1,
        'reporter': 'k.marzec',
        'data': {
            'channel': 'controlling',
            'workspace': 'finance'
        }
    },
    {
        'title': 'ticket_8',
        'description': 'some another desc',
        'status': 'done',
        'severity': 'medium',
        'namespace_id': 3,
        'reporter': 'a.olech',
        'data': {
            'channel': 'payments',
            'workspace': 'hr'
        }
    },
    {
        'title': 'ticket_9',
        'description': 'some description',
        'status': 'not started',
        'severity': 'low',
        'namespace_id': 2,
        'reporter': 'k.marzec',
        'data': {
            'channel': 'accountancy',
            'workspace': 'finance'
        }
    },
    {
        'title': 'ticket_10',
        'description': 'some_description',
        'status': 'doing',
        'severity': 'medium',
        'namespace_id': 2,
        'reporter': 'a.olech',
        'data': {
            'channel': 'payments',
            'workspace': 'hr'
        }
    },
    {
        'title': 'ticket_11',
        'description': 'some_description',
        'status': 'done',
        'severity': 'low',
        'namespace_id': 1,
        'reporter': 'a.olech',
        'data': {
            'channel': 'payments',
            'workspace': 'hr'
        }
    },
]

