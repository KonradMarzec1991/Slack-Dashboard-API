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
            text = 'Your tickets\n'
            for ticket in tickets:
                text += f'{ticket.title.capitalize()}\n'
                text += f'{ticket.description}\n'
                text += f'status: {ticket.status}\n'
                text += f'severity: {ticket.severity}\n'
                text += f'created at: {ticket.created_at}\n'
                text += '{"type": "divider"}'

        return self.send_message(
            channel_id=self.channel_id,
            text=text
        )
