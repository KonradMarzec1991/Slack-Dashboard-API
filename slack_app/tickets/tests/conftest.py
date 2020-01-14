import json
import pytest

from tickets.models import Ticket


@pytest.fixture
def tickets_data():

    def load_fixture_from_json(json_path):
        with open(json_path) as f:
            return json.load(f)

    t_list = load_fixture_from_json('../../fixtures/tickets.json')
    for t_item in t_list:
        Ticket.objects.create(**t_item['fields'])

