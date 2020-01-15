"""
Slack actions for interactions with db/server
"""

import requests


class Actions:

    def __init__(self, provider, channel_id, user):
        self.provider = provider
        self.channel_id = channel_id
        self.user = user

    def show_tickets(self, tickets):
        if not tickets.all():
            text = 'You do not have any tickets'
        else:
            text = 'Your tickets\n'
            for ticket in tickets:
                text += f'{ticket.title.capitalize()}\n'
                text += f'{ticket.description}\n'
                text += f'status: {ticket.status}\n'
                text += f'severity: {ticket.severity}\n'
                text += f'created at: {ticket.created_at}\n'

        return self.provider.send_message(
            channel_id=self.channel_id,
            text=text
        )

    def create_dialog(self, trigger_id):

        post_url = 'https://slack.com/api/dialog.open'

        data = {
            'token': self.provider.token,
            'trigger_id': trigger_id,
            'dialog': self.provider.display_dialog()
        }

        resp = requests.post(
            url=post_url,
            data=data
        )
        return resp
