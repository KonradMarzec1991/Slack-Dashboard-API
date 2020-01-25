from celery import shared_task

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import requests
import json

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from tickets.models import Ticket, Namespace
from .actions import Actions


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
        return HttpResponse(status=200)


@csrf_exempt
def display_dialog(request):
    request_data = request.POST
    a = Actions(request_data['channel_id'])
    content = a.display_dialog(request_data['trigger_id'], action_type='create_ticket')

    if not content['ok']:
        return HttpResponse('Something went wrong, please try again...')
    return HttpResponse(status=200)


@csrf_exempt
def proceed_payload(request):

    data = request.POST
    data_dict = json.loads(data['payload'])

    print(data_dict)

    reporter = data_dict['user']['name']  # user name

    channel_id = data_dict['channel']['id']  # channel JSON
    team_id = data_dict['team']['id']  # workspace JSON

    a = Actions(channel_id)

    if data_dict['type'] == 'block_actions':

        action_id = data_dict['actions'][0]['action_id']
        type_action = action_id[0]
        ticket_id = int(action_id[1:])

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            a.send_message(
                channel_id=channel_id,
                text=f'This ticket has been removed! Please refreash list with `\show_tickets`.'
            )
            return HttpResponse(status=200)

        if type_action == 'E':
            a.display_dialog(data_dict['trigger_id'], action_type='edit_ticket', ticket=ticket)
        elif type_action == 'D':

            ticket.delete()
            a.send_message(
                channel_id=channel_id,
                text=f'`Ticket {ticket_id}` has been removed.'
            )

        return HttpResponse(status=200)

    if data_dict['type'] == 'dialog_cancellation':

        if data_dict['callback_id'] == 'edit_ticket':

            ticket_id = data_dict['state']

            a.send_message(
                channel_id=channel_id,
                text=f'*Modification* of `ticket {ticket_id}` has been cancelled.'
            )
            return HttpResponse(status=200)

        elif data_dict['callback_id'] == 'create_ticket':

            a.send_message(
                channel_id=channel_id,
                text='*Creation* of `ticket` has been cancelled.'
            )
            return HttpResponse(status=200)

    if data_dict['type'] == 'dialog_submission':

        if data_dict['callback_id'] == 'create_ticket':

            def create_ticket(data_dict, channel_id, team_id):
                title = data_dict['submission']['title']
                description = data_dict['submission']['description']
                status = data_dict['submission']['status']
                severity = data_dict['submission']['severity']

                workspace = a.get_workspace(team_id)
                channel = a.get_channel(channel_id)

                ticket_data = {
                    'namespace': Namespace.objects.get(id=1),  # temporary solution
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
                ticket = Ticket.objects.create(**ticket_data)
                return ticket

            create_ticket(data_dict, channel_id, team_id)

            a.send_message(
                channel_id=channel_id,
                text='Ticket has been created'
            )

            return HttpResponse(status=200)

        elif data_dict['callback_id'] == 'edit_ticket':

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

            a.send_message(
                channel_id=channel_id,
                text=f'`Ticket {ticket_id}` has been modified.'
            )
            return HttpResponse(status=200)


@shared_task
def create_ticket(ticket_data, response_url):

    Ticket.objects.create(**ticket_data)
    a = Actions()
    data = json.dumps({
        'token': a.token,
        'text': 'Ticket has been created'
    })

    response = requests.post(response_url, data=data)
    return HttpResponse(status=200)
