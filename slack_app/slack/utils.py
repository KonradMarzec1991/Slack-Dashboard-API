import json
from collections import abc

import requests
from celery import shared_task

from slack.actions import Actions
from tickets.models import Namespace, Ticket


class FrozenJSON:
    """
    A read-only façade for navigating a JSON-like object
    using attribute notation
    """

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


@shared_task
def create_ticket(data_dict, reporter, channel_id, team_id, response_url):
    a = Actions(channel_id)

    title = data_dict['submission']['title']
    description = data_dict['submission']['description']
    status = data_dict['submission']['status']
    severity = data_dict['submission']['severity']

    workspace = a.get_workspace(team_id)
    channel = a.get_channel(channel_id)

    ticket_data = {
        'namespace': Namespace.objects.get(id=1),  # temporary solution
        'title': title,
        'description': description,
        'status': status,
        'severity': severity,
        'reporter': reporter,
        'data': {
            'channel': channel,
            'workspace': workspace
        }
    }
    Ticket.objects.create(**ticket_data)
    data = json.dumps({
        'token': a.token,
        'text': 'Ticket has been created'
    })

    requests.post(response_url, data=data)
    return {'status': 200}


