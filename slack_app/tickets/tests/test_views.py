import pytest
from rest_framework.test import APIClient
from tickets.models import Ticket, Namespace


@pytest.mark.django_db(transaction=True)
class TestExperiment:

    def get_client(self, url=None):
        client = APIClient()
        if url is None:
            response = client.get('/tickets/')
        else:
            response = client.get(f'/tickets/?{url}')
        return response

    def test_namespace_view(self, tickets):
        client = APIClient()
        response = client.get('/namespace/')
        assert response.status_code == 200
        assert len(response.json()) == 3

    # def test_ticket_view_no_params(self, namespaces, tickets):
    #     client = self.get_client()




