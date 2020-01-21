from celery import shared_task

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import requests
import json

from tickets.models import Ticket, Namespace
from .provider import Provider
from .actions import Actions


URL_POST_MESSAGE = 'https://slack.com/api/chat.postMessage'


@csrf_exempt
def display_information(request):
    channel_id = request.POST.get('channel_id')
    actions = Actions(channel_id)

    actions.send_message(
        channel_id=channel_id,
        blocks=json.dumps(
            actions.slack_information()
        )
    )
    return HttpResponse(status=200)


@csrf_exempt
def show_my_tickets(request):
    reporter = request.POST.get('user_name')
    channel_id = request.POST.get('channel_id')
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
    response = requests.post('https://slack.com/api/chat.postMessage', data=data)
    print(response.text)
    return HttpResponse(status=200)


@csrf_exempt
def display_dialog(request):
    request_data = request.POST
    a = Actions(request_data['channel_id'])
    content = a.display_dialog(request_data['trigger_id'])

    if not content['ok']:
        return HttpResponse('Something went wrong, please try again...')
    return HttpResponse(status=200)


@csrf_exempt
def proceed_payload(request):
    data = request.POST
    print(data)

    data_dict = json.loads(data['payload'])

    reporter = data_dict['user']['name']  # user name

    channel_id = data_dict['channel']['id']  # channel JSON
    team_id = data_dict['team']['id']  # workspace JSON

    a = Actions(channel_id)

    if data_dict['type'] == 'block_actions':

        action_id = data_dict['actions'][0]['action_id']
        type_action = action_id[0]
        ticket_id_action = action_id[1:]

        if type_action == 'E':
            pass
            a.display_dialog(data_dict['trigger_id'])
        else:
            a.send_message(
                channel_id=channel_id,
                text=f'Sth to return'
            )
        return HttpResponse(status=200)

    if data_dict['type'] == 'dialog_cancellation':
        a.send_message(
            channel_id=channel_id,
            text='Creation of ticket has been cancelled'
        )
        return HttpResponse(status=200)

    if data_dict['type'] == 'dialog_submission':

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


@shared_task
def create_ticket(ticket_data, response_url):

    Ticket.objects.create(**ticket_data)
    p = Provider()
    data = json.dumps({
        'token': p.token,
        'text': 'Ticket has been created'
    })

    response = requests.post(response_url, data=data)
    return HttpResponse(status=200)
