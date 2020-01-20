"""
Slack actions for interactions with db/server
Overrides methods of provider to simplify using them
"""


from .provider import Provider


class Actions(Provider):

    def __init__(self, channel_id):
        super().__init__()
        self.channel_id = channel_id

    def show_tickets(self, tickets):
        if not tickets.exists():
            text = 'You do not have any tickets'
        else:
            text = []
            for ticket in tickets:
                text.append(self.template_ticket(ticket))
        return text

    def template_ticket(self, ticket):
        template = \
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Title:*\n{ticket.title.capitalize()}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{ticket.description}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Status:*\n{ticket.status}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:*\n{ticket.severity}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Created at:*\n{ticket.created_at}"
                }
            ]
        },
        # {
        #     "type": "actions",
        #     "elements": [
        #         {
        #             "type": "button",
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "Edit"
        #             },
        #             "style": "primary",
        #             "value": "click_me_123"
        #         },
        #         {
        #             "type": "button",
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "Delete"
        #             },
        #             "style": "danger",
        #             "value": "click_me_123"
        #         }
        #     ]
        # },
        # {
        #     "type": "divider"
        # },

        return template
