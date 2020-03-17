from celery import shared_task

from .utils import create_ticket, FrozenJSON
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import requests
import json

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from tickets.models import Ticket, Namespace
from .actions import Actions

import logging
logger = logging.getLogger(__name__)


class SlackInformationViewSet(ViewSet):

    permission_classes = (AllowAny, )

    def create(self, request):
        channel_id = request.POST['channel_id']
        actions = Actions(channel_id)

        actions.send_message(
            channel_id=channel_id,
            blocks=json.dumps(
                actions.slack_information()
            )
        )
        return Response(status=200)


class SlackTicketsListViewSet(ViewSet):

    def create(self, request):
        reporter = request.POST['user_name']
        channel_id = request.POST['channel_id']

        user_tickets = Ticket.objects.filter(
            reporter=reporter
        )
        a = Actions(channel_id)
        blocks = a.show_tickets(user_tickets)

        data = {
            'token': a.token,
            'channel': channel_id,
            'blocks': json.dumps(blocks)

        }
        requests.post(a.URL_SEND_MESSAGE, data=data)
        return Response(status=200)


class SlackDialogViewSet(ViewSet):

    def create(self, request):
        request_data = request.POST

        channel_id = request_data['channel_id']
        trigger_id = request_data['trigger_id']

        a = Actions(channel_id)
        content = a.display_dialog(
            trigger_id=trigger_id,
            action_type='create_ticket'
        )
        if not content['ok']:
            return Response(
                'Something went wrong, please try again...'
            )
        return Response(status=200)


@csrf_exempt
def proceed_payload(request):

    data = request.POST
    data_dict = json.loads(data['payload'])

    feed = FrozenJSON(data_dict)

    reporter = feed.user.name
    channel_id = feed.channel.id
    team_id = feed.team.id

    actions = Actions(channel_id)

    response_url = feed.response_url

    if feed.type == 'block_actions':

        # action_id = data_dict['actions'][0]['action_id']
        action_id = feed.actions[0].action_id
        type_action = action_id[0]
        ticket_id = int(action_id[1:])

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            actions.send_message(
                channel_id=channel_id,
                text=f'This ticket has been removed! '
                     f'Please refreash list with `\show_tickets`'
            )
            return HttpResponse(status=200)

        if type_action == 'E':
            actions.display_dialog(data_dict['trigger_id'],
                             action_type='edit_ticket',
                             ticket=ticket)
        elif type_action == 'D':
            ticket.delete()
            actions.send_message(
                channel_id=channel_id,
                text=f'`Ticket {ticket_id}` has been removed.'
            )

        return HttpResponse(status=200)

    if feed.type == 'dialog_cancellation':

        if data_dict['callback_id'] == 'edit_ticket':

            ticket_id = data_dict['state']

            actions.send_message(
                channel_id=channel_id,
                text=f'*Modification* of `ticket id:{ticket_id}` has been cancelled.'
            )
            return HttpResponse(status=200)

        elif feed.callback_id == 'create_ticket':

            actions.send_message(
                channel_id=channel_id,
                text='*Creation* of `ticket` has been cancelled.'
            )
            return HttpResponse(status=200)

    if feed.type == 'dialog_submission':

        if feed.callback_id == 'create_ticket':

            create_ticket.delay(
                data_dict,
                reporter,
                channel_id,
                team_id,
                response_url
            )

            actions.send_message(
                channel_id=channel_id,
                text='Processing request...'
            )

            return HttpResponse(status=200)

        elif feed.callback_id == 'edit_ticket':

            ticket_id = int(data_dict['state'])

            ticket = Ticket.objects.get(id=ticket_id)

            title = data_dict['submission']['title']
            description = data_dict['submission']['description']
            status = data_dict['submission']['status']
            severity = data_dict['submission']['severity']

            ticket.title = title
            ticket.description = description
            ticket.status = status
            ticket.severity = severity

            ticket.save()

            actions.send_message(
                channel_id=channel_id,
                text=f'`Ticket id:{ticket_id}` has been modified.'
            )
            return HttpResponse(status=200)



