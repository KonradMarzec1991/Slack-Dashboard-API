"""
Slack actions for interactions with db/server
Overrides methods of provider to simplify using them
"""

import os
import json

import requests
from django.http import HttpResponse

from .templates import Templates


class Actions(Templates):

    def __init__(self, channel_id):
        self.token = os.getenv('SLACK_TOKEN')
        self.channel_id = channel_id

    def show_tickets(self, tickets):
        text = []
        if not tickets.exists():
            text.append(self.tickets_main_section(
                "*:star: You do not have any tickets :star:*"))
        else:
            text.append(self.tickets_main_section(
                "*:star: Your tickets: :star:*"))
            for ticket in tickets:
                text.append(self.ticket_section(ticket))
                text.append(self.ticket_buttons(ticket.id))
                text.append(self.ticket_divider())
        return text

    def get_channel(self, channel_id):
        """
        :param channel_id: channel ID from Slack API
        :return: channel name (private channel)
        """
        data = {
            'token': self.token,
            'channel': channel_id
        }
        res = requests.post(os.getenv('URL_CHANNEL_NAME'), data=data)
        response = json.loads(res.content)
        return response['channel']['name']

    def get_workspace(self, team_id):
        """
        :param team_id: team/workspace ID from Slack API
        :return: workspace name
        """
        data = {
            'token': self.token,
            'team': team_id
        }
        res = requests.post(os.getenv('URL_WORKSPACE_NAME'), data=data)
        response = json.loads(res.content)
        return response['team']['name']

    def send_message(self, text=None, blocks=None):
        """
        :param channel_id: channel ID from Slack API
        :param text: message text
        :param blocks: slack blocks for formatting message
        :return: message to user via Slack
        """
        data = {
            'token': self.token,
            'channel': self.channel_id,
            'text': text if text else None,
            'blocks': blocks if blocks else None
        }

        requests.post(os.getenv('URL_SEND_MESSAGE'), data=data)
        return HttpResponse(status=200)

    def display_dialog(self, trigger_id, action_type, ticket=None):
        dialog = {
            "callback_id": action_type,
            "title": "Create ticket",
            "submit_label": "Submit",
            "notify_on_cancel": True,
            "state": ticket.id if ticket else "Create todo",
            "elements": [
                {
                    "label": "Title",
                    "name": "title",
                    "type": "text",
                    "placeholder": "my ticket...",
                    "value": str(ticket.title.capitalize()) if ticket else None,
                },
                {
                    "label": "Description",
                    "name": "description",
                    "type": "textarea",
                    "hint": "Provide details of ticket",
                    "value": str(ticket.description) if ticket else None,

                },
                {
                    "label": "Status",
                    "name": "status",
                    "type": "select",  # value to populated in editing
                    "value": str(ticket.status) if ticket else None,
                    "options": [
                        {
                            "label": "not started",
                            "value": "not started"
                        },
                        {
                            "label": "doing",
                            "value": "doing"
                        },
                        {
                            "label": "done",
                            "value": "done"
                        }
                    ]
                },
                {
                    "label": "Severity",
                    "name": "severity",
                    "type": "select",
                    "value": str(ticket.severity) if ticket else None,
                    "options": [
                        {
                            "label": "low",
                            "value": "low"
                        },
                        {
                            "label": "medium",
                            "value": "medium"
                        },
                        {
                            "label": "high",
                            "value": "high"
                        }
                    ]
                }
            ]
        }

        data = {
            'token': self.token,
            'trigger_id': trigger_id,
            'dialog': json.dumps(dialog)
        }
        response = requests.post(os.getenv('URL_DIALOG_OPEN'), data=data)
        return json.loads(response.content)
