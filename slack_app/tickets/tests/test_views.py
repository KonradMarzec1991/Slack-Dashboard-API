import pytest
from rest_framework.test import APIClient, APIRequestFactory
from tickets.views import NamespaceViewSet
from rest_framework import status


@pytest.mark.django_db(reset_sequences=True)
class TestNamespaceView:

    def test_list_view(self, namespaces):

        def _get(path, view_type):
            request = APIRequestFactory().get(path)
            view = NamespaceViewSet.as_view({'get': view_type})
            return view(request)

        response = _get('/namespace/', 'list')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_retrieve_view(self, namespaces):
        response = APIClient().get('/namespace/1/')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)
        assert response.data.get('name') == 'teamwork'














