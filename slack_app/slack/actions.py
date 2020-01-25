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

    @staticmethod
    def slack_information():
        template = \
        [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Hey there* 👋 I'm TicketBot. I'm here to help you create and manage tickets in Slack.\n"
                            "There are two commands to manage/create tasks:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*1️⃣ `/show_tickets` command*. "
                            "Type `/show_tickets-tasks` to displays all your current unclosed tickets"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*2️⃣ `/create` command*. "
                            "Type `/create` to open dialog form and create ticket"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":star: Have fun!!! :star:"
                }
            }
        ]
        return template

    @staticmethod
    def tickets_main_section(text):
        template = \
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        return template

    @staticmethod
    def ticket_section(ticket):
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
        }
        return template

    @staticmethod
    def ticket_buttons(ticket_id):
        template = \
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Edit"
                    },
                    "style": "primary",
                    "action_id": f'E{ticket_id}'
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Delete"
                    },
                    "style": "danger",
                    "action_id": f'D{ticket_id}'
                }
            ]
        }
        return template

    @staticmethod
    def ticket_divider():
        return {"type": "divider"}
