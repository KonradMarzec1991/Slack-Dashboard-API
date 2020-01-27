import pytest
from rest_framework.test import APIClient, APIRequestFactory
from tickets.views import NamespaceViewSet
from tickets.models import Namespace
from rest_framework import status


@pytest.mark.django_db(reset_sequences=True)
class TestNamespaceView:

    def client(self):
        return APIClient()

    def test_list_view(self, namespaces):

        def _get(path, view_type):
            request = APIRequestFactory().get(path)
            view = NamespaceViewSet.as_view({'get': view_type})
            return view(request)

        response = _get('/namespace/', 'list')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_retrieve_view(self, namespaces):
        response = self.client().get('/namespace/1/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('name') == 'teamwork'

    def test_post(self):
        response = self.client().post('/namespace/', {'name': 'chernobyl'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'id': 1, 'name': 'chernobyl'}

    def test_put(self, namespaces):
        response = self.client().put('/namespace/1/', {'name': 'chernobyl'})
        assert response.status_code == status.HTTP_200_OK
        chernobyl = Namespace.objects.get(pk=1)
        assert chernobyl.name == 'chernobyl'

    def test_delete(self, namespaces):
        response = self.client().delete('/namespace/1/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(Namespace.objects.all()) == 2

















