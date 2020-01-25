"""
Slack resource providing basic methods to interact with Slack API.
It covers:
    - getting channel id / name
    - getting workspace id / name
    - posting message
"""

import json

import requests
from django.http import HttpResponse


class Provider:
    """
    Basic methods provider for Slack communication
    """

    URL_CHANNEL_NAME = 'https://slack.com/api/conversations.info'
    URL_WORKSPACE_NAME = 'https://slack.com/api/team.info'
    URL_SEND_MESSAGE = 'https://slack.com/api/chat.postMessage'
    URL_DIALOG_OPEN = 'https://slack.com/api/dialog.open'

    def __init__(self):
        self.token = ''

    def get_channel(self, channel_id):
        """
        :param channel_id: channel ID from Slack API
        :return: channel name (private channel)
        """
        data = {
            'token': self.token,
            'channel': channel_id
        }
        res = requests.post(self.URL_CHANNEL_NAME, data=data)
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
        res = requests.post(self.URL_WORKSPACE_NAME, data=data)
        response = json.loads(res.content)
        return response['team']['name']

    def send_message(self, channel_id, text=None, blocks=None):
        """
        :param channel_id: channel ID from Slack API
        :param text: message text
        :param blocks: slack blocks for formatting message
        :return: message to user via Slack
        """
        data = {
            'token': self.token,
            'channel': channel_id,
            'text': text if text else None,
            'blocks': blocks if blocks else None
        }

        response = requests.post(self.URL_SEND_MESSAGE, data=data)
        return HttpResponse(status=200)

    def display_dialog(self, trigger_id, action_type, ticket=None):
        """
        :param trigger_id: trigger value of Slack event
        :return: opens dialog window to user
        """
        # dialog = {
        #     "callback_id": action_type,
        #     "title": "Create ticket",
        #     "submit_label": "Submit",
        #     "notify_on_cancel": True,
        #     "state": ticket.id if ticket else "Create ticket",
        #     "elements": [
        #         {
        #             "label": "Title",
        #             "name": "title",
        #             "type": "text",
        #             "placeholder": "my ticket...",
        #             "value": str(ticket.title.capitalize()) if ticket else None,
        #         },
        #         {
        #             "label": "Description",
        #             "name": "description",
        #             "type": "textarea",
        #             "hint": "Provide details of ticket",
        #             "value": str(ticket.description) if ticket else None,
        #
        #         },
        #         {
        #             "label": "Status",
        #             "name": "status",
        #             "type": "select",  # value to populated in editing
        #             "value": str(ticket.status) if ticket else None,
        #             "options": [
        #                 {
        #                     "label": "not started",
        #                     "value": "not started"
        #                 },
        #                 {
        #                     "label": "doing",
        #                     "value": "doing"
        #                 },
        #                 {
        #                     "label": "done",
        #                     "value": "done"
        #                 }
        #             ]
        #         },
        #         {
        #             "label": "Severity",
        #             "name": "severity",
        #             "type": "select",
        #             "value": str(ticket.severity) if ticket else None,
        #             "options": [
        #                 {
        #                     "label": "low",
        #                     "value": "low"
        #                 },
        #                 {
        #                     "label": "medium",
        #                     "value": "medium"
        #                 },
        #                 {
        #                     "label": "high",
        #                     "value": "high"
        #                 }
        #             ]
        #         }
        #     ]
        # }

        view = {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "Ticket creation",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "title",
                    "label": {
                        "type": "plain_text",
                        "text": "Ticket title"
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_input",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "name..."
                        }
                    }
                },
                {
                    "type": "input",
                    "block_id": "description",
                    "label": {
                        "type": "plain_text",
                        "text": "Ticket description",
                    },
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "description..."
                        }
                    },
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": "Choose status level",
                        "emoji": True
                    },
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select status...",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "not started",
                                    "emoji": True
                                },
                                "value": "not started"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "doing",
                                    "emoji": True
                                },
                                "value": "doing"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "done",
                                    "emoji": True
                                },
                                "value": "done"
                            }
                        ]
                    }
                },
                {
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": "Choose status level",
                        "emoji": True
                    },
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select status...",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "not started",
                                    "emoji": True
                                },
                                "value": "not started"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "doing",
                                    "emoji": True
                                },
                                "value": "doing"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "done",
                                    "emoji": True
                                },
                                "value": "done"
                            }
                        ]
                    }
                }
            ]
        }

        data = {
            'token': self.token,
            'trigger_id': trigger_id,
            'view': json.dumps(view)
        }
        response = requests.post('https://slack.com/api/views.open', data=data)
        return json.loads(response.content)
