"""
Slack actions for interactions with db/server
"""

import requests

from .provider import Provider


class Actions:

    def __init__(self, provider, channel_id, user):
        self.provider = provider
        self.channle_id = channel_id
        self.user = user

    def show_tasks(self, tickets):
        if not tickets.all():
            text = 'You do not have any tickets'
        else:
            text = 'Your tickets\n'
            for ticket in tickets:
                pass

        return self.provider.postmessage(
            #  fill
        )

    def create_dialog(self, trigger_id, create_text=None):

        post_url = '...'

        data = {
            'token': '',
            'trigger_id': trigger_id,
            'dialog': ''
        }

        resp = requests.post(
            url=post_url,
            data=data
        )
        return resp
