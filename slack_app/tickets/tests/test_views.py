import pytest
from rest_framework.test import (
    APIClient,
    APIRequestFactory
)

from tickets.views import (
    NamespaceViewSet,
    TicketViewSet
)

from tickets.models import Namespace
from rest_framework import status


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('namespaces')
class TestNamespaceView:

    def client(self):
        return APIClient()

    def test_list(self):
        def _get(path, view_type):
            request = APIRequestFactory().get(path)
            view = NamespaceViewSet.as_view({'get': view_type})
            return view(request)

        response = _get('/namespaces/', 'list')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_retrieve(self):
        response = self.client().get('/namespaces/1/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == 'teamwork'

    def test_post(self):
        response = self.client().post('/namespaces/', {'name': 'chernobyl'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'id': 4, 'name': 'chernobyl'}

    def test_put(self):
        response = self.client().put('/namespaces/1/', {'name': 'chernobyl'})
        assert response.status_code == status.HTTP_200_OK
        chernobyl = Namespace.objects.get(pk=1)
        assert chernobyl.name == 'chernobyl'

    def test_delete(self):
        response = self.client().delete('/namespaces/1/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(Namespace.objects.all()) == 2


@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.usefixtures('tickets')
class TestNamespaceTicketView:

    def client(self):
        return APIClient()

    @pytest.mark.parametrize(
        'namespace_id, num_of_tickets, num_of_pages, h_status',
        [
            (1, 6, 2, status.HTTP_200_OK),
            (2, 4, 1, status.HTTP_200_OK),
            (3, 1, 1, status.HTTP_200_OK)
        ]
    )
    def test_list(self, namespace_id, num_of_tickets, num_of_pages, h_status):
        response = self.client().get(f'/namespaces/{namespace_id}/tickets/')

        assert response.status_code == h_status
        assert response.data['list']['num_of_tickets'] == num_of_tickets
        assert response.data['list']['num_of_pages'] == num_of_pages

    @pytest.mark.parametrize(
        'namespace_id, ticket_id, h_status',
        [
            (1, 1, status.HTTP_200_OK),
            (2, 2, status.HTTP_404_NOT_FOUND),
            (3, 3, status.HTTP_404_NOT_FOUND),
            (3, 8, status.HTTP_200_OK),
            (2, 3, status.HTTP_200_OK),
            (1, 6, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_retrieve(self, namespace_id, ticket_id, h_status):
        response = self.client().get(
            f'/namespaces/{namespace_id}/tickets/{ticket_id}/'
        )

        assert response.status_code == h_status

    def test_post(self):
        test_ticket = {
            'title': 'ticket_PI3.14',
            'description': 'math.PI',
            'severity': 'low',
            'status': 'doing',
            'namespace': 'teamwork',
            'reporter': 'k.marzec',
            'data': {
                'channel': 'controlling',
                'workspace': 'finance'
            }
        }
        factory = APIRequestFactory()
        request = factory.post(
            f'/namespaces/1/tickets/', {**test_ticket}, format='json')
        view = TicketViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'id': 12, **test_ticket}

    def test_put(self):
        pass

    def test_delete(self):
        pass

























