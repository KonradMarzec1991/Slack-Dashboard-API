"""
Slack resource providing basic methods to interact with Slack API.
It covers:
    - getting channel id / name
    - getting workspace id / name
    - posting message
"""

import requests


URL_CHANNEL_NAME = 'https://slack.com/api/conversations.info'
URL_WORKSPACE_NAME = 'https://slack.com/api/team.info'
URL_SEND_MESSAGE = 'https://slack.com/api/chat.postEphemeral'


def get_channel(token, channel_id):
    data = {
        'token': token,
        'channel': channel_id
    }
    response = requests.post(URL_CHANNEL_NAME, data=data)
    return response['channel']['name']


def get_workspace(token, team_id):
    data = {
        'token': token,
        'team': team_id
    }
    response = requests.post(URL_WORKSPACE_NAME, data=data)
    return response['team']['name']


def send_message(token, channel_id, attachements, text, user):
    data = {
        'token': token,
        'channel': channel_id,
        'attachments': attachements,

    }





