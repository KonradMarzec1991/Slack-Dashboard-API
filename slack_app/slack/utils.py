import json
from collections import abc

import requests
from celery import shared_task

from slack.actions import Actions
from tickets.models import Namespace, Ticket

CANCELLED = '*Creation* of `ticket` has been cancelled.'
PROCESS = 'Processing request...'
ALREADY_REMOVED = f'This ticket has been removed! Please refreash list with `"\"show_tickets`'
GONE_WRONG = 'Something went wrong, please try again...'


class FrozenJSON:
    """
    A read-only façade for navigating a JSON-like object
    using attribute notation
    """

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        # pylint: disable=no-else-return
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        # pylint: disable=no-else-return
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


@shared_task
def create_ticket(data_dict, reporter, channel_id, team_id, response_url):
    """
    :return: ticket of user saved in db
    """
    actions = Actions(channel_id)
    feed = FrozenJSON(data_dict)

    title, description, status, severity = \
        get_basic_ticket_attr(feed, submission=True)

    workspace = actions.get_workspace(team_id)
    channel = actions.get_channel(channel_id)

    ticket_data = {
        'namespace': Namespace.objects.get(id=1),  # pylint: disable=no-member
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
        'token': actions.token,
        'text': 'Ticket has been created'
    })

    requests.post(response_url, data=data)
    return {'status': 200}


def get_basic_ticket_attr(feed, submission=False):
    """
    :param feed: Slack dictionary response
    :param submission: True if user wants to create tickets, else False
    :return: tuple with basic ticket information
    """
    if submission:
        return (feed.submission.title, feed.submission.description,
                feed.submission.status, feed.submission.severity)
    return feed.title, feed.description, feed.status, feed.severity
