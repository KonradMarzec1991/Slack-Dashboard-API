"""
class `Templates` delivers slack API templates for interaction with user
"""


class Templates:

    @staticmethod
    def slack_information():
        return \
            [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Hey there* 👋 I'm TicketBot. "
                                "I'm here to help you create and "
                                "manage tickets in Slack.\n"
                                "There are two commands "
                                "to manage/create tasks:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*1️⃣ `/show_tickets` command*. "
                                "Type `/show_tickets-tasks` to displays all"
                                " your current unclosed tickets"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*2️⃣ `/create` command*. "
                                "Type `/create` to open dialog "
                                "form and create ticket"
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

    @staticmethod
    def tickets_main_section(text):
        return \
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }

    @staticmethod
    def ticket_section(ticket):
        return \
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

    @staticmethod
    def ticket_buttons(ticket_id):
        return \
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

    @staticmethod
    def ticket_divider():
        return {"type": "divider"}