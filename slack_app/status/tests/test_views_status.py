import pytest
from django.test import Client


@pytest.fixture
def status_values():
    return {
        'commit': '2874#952',
        'version': '1.0.0'
    }


def status_response(key=None):
    client = Client()
    if key is None:
        response = client.get('http://127.0.0.1:8000/status/')
    else:
        response = client.get(f'http://127.0.0.1:8000/status/{key}')
    return response


# def test_status_view_response(status_values):
#     response = status_response()
#     assert response.status_code == 200
#     assert response.data == status_values
#
#
# def test_status_view_response_key():
#     response = status_response('commit')
#     assert response.status_code == 200
#     response = status_response('_wrong')
#     assert response.status_code == 404


from unittest import TestCase


class StatusViewTestCase(TestCase):

    def setUp(self):
        self.values = {'commit': '2874#952', 'version': '1.0.0'}
        self.client = Client()

    def test_status_response_view(self):
        response = self.client.get('http://127.0.0.1:8000/status/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.values)
