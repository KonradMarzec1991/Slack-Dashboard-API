from celery import shared_task

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf import settings
import requests
import json
from tickets.models import Ticket


SLACK_TOKEN = settings.SLACK_TOKEN
URL_DIALOG_OPEN = 'https://slack.com/api/dialog.open'
URL_POST_MESSAGE = 'https://slack.com/api/chat.postMessage'


@csrf_exempt
def testview(request):
    if request.method == "POST":
        print(request.POST)
        token = 'xoxb-676821839270-682460664294-42dMAoDFZvIIshCPkJjeWrCg'
        channel_id = request.POST.get('channel_id')
        data = {
            'token': token,
            'channel_id': channel_id
        }
        resp = requests.post('https://slack.com/api/conversations.info', data=data)
        print(resp.content)
        return HttpResponse('aaaa')


@csrf_exempt
def display_dialog(request):

    request_data = request.POST
    text = request_data['text']

    dialog = {
        "callback_id": "ryde-46e2b0",
        "title": "Create todo",
        "submit_label": "Submit",
        "notify_on_cancel": True,
        "state": "Limo",
        "elements": [
            {
                "label": "Title",
                "name": "title",
                "type": "text",
                "placeholder": "my ticket..."
            },
            {
                "label": "Description",
                "name": "description",
                "type": "textarea",
                "hint": "Provide details of ticket"

            },
            {
                "label": "Status",
                "name": "status",
                "type": "select",
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
        'token': SLACK_TOKEN,
        'trigger_id': request_data['trigger_id'],
        'dialog': json.dumps(dialog)
    }

    response = requests.post(URL_DIALOG_OPEN, data=data)
    content = json.loads(response.content)

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

    if data_dict['type'] == 'dialog_cancellation':

        data = {
            'token': SLACK_TOKEN,
            'channel': channel_id,
            'text': 'Ticket has been cancelled'
        }

        response = requests.post(URL_POST_MESSAGE, data=data)
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
