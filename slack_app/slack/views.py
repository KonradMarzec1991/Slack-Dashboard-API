from celery import shared_task

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import requests
import json
from tickets.models import Ticket


from .provider import Provider
from .actions import Actions


SLACK_TOKEN = ''
URL_DIALOG_OPEN = 'https://slack.com/api/dialog.open'
URL_POST_MESSAGE = 'https://slack.com/api/chat.postMessage'


@csrf_exempt
def display_dialog(request):

    request_data = request.POST
    print(request_data)
    p = Provider()
    a = Actions(request_data['channel_id'])
    # content = p.display_dialog(request_data['trigger_id'])
    content = a.display_dialog(request_data['trigger_id'])
    print(content)

    if not content['ok']:
        return HttpResponse('Something went wrong, please try again...')
    return HttpResponse(status=200)


@csrf_exempt
def proceed_payload(request):

    data = request.POST

    data_dict = json.loads(data['payload'])

    reporter = data_dict['user']['name']  # user name

    channel_id = data_dict['channel']['id']  # channel JSON
    team_id = data_dict['team']['id']  # workspace JSON

    p = Provider()

    workspace = p.get_workspace(team_id)
    channel = p.get_channel(channel_id)

    if data_dict['type'] == 'dialog_cancellation':
        p.send_message(
            channel_id,
            'Creation of ticket has been cancelled'
        )
        return HttpResponse(status=200)

    data = {
        'token': SLACK_TOKEN,
        'channel': channel_id,
        'text': 'Processing request...'
    }

    title = data_dict['submission']['title']
    description = data_dict['submission']['description']
    status = data_dict['submission']['status']
    severity = data_dict['submission']['severity']

    response_url = data_dict['response_url']

    ticket_data = {
        'title': title,
        'description': description,
        'status': status,
        'severity': severity,
        'reporter': reporter,
        'data': json.dumps({
            'channel': channel_id,
            'team_id': team_id
        })
    }

    task = create_ticket.delay(ticket_data, response_url)

    response = requests.post(URL_POST_MESSAGE, data=data)

    return HttpResponse(status=200)


@shared_task
def create_ticket(ticket_data, response_url):

    Ticket.objects.create(**ticket_data)

    data = json.dumps({
        'token': SLACK_TOKEN,
        'text': 'Ticket has been created'
    })

    response = requests.post(response_url, data=data)
    return HttpResponse(status=200)
