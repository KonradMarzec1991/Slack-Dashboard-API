# Slack tickets Dashboard

This is an example application that uses Django for communication with Slack API.
### Installing

Below terminal commands allow run app in development mode

```
git clone https://github.com/KonradMarzec1991/slack_app.git

```
### Slack Access
In order to fully use application, install Slack app 
for communication with Django server - 
how to do this https://api.slack.com/start<br>

After installation, register `slash commands` and `interactivity request url`:
* create
* show_tickets
* information (facultative)

Add below permissions to allow API get channel/workspace names or send message:
```
channels:read
groups:read
groups:write
im:readv
mpim:read
team:read
chat:write:user
incoming-webhook
commands
```


### Exposing localhost server
To enable Slack communication with server, expose localhost server.
One of options how to do this - https://ngrok.com/<br>
Example how to use **ngrok**:
```
ngrok localhost 8000
```
It generates tunnel address `http://50b7554e.ngrok.io`. 
Then Slack commands urls will look like:
```
create - http://50b7554e.ngrok.io/display_dialog
show_tickets - http://50b7554e.ngrok.io/show_tickets
information - http://50b7554e.ngrok.io/display_information

Interactivity request URL - http://50b7554e.ngrok.io/proceed_payload
```

### Features

Slack integration API enables CRUD operations on tickets with commands:
* **\create** - opens Slack modal window (form), that allows when filled and 
submitted, creation of user's ticket
* **\show_tickets** - displays Slack block of user's tickets with options 
to edit and delete
* **\information** - delivers basic description of how to use above commands

Django API additionally devliers:
* pagination
* filtering options using url params:
    * name or description
    * reporter (owner/creator)
    * workspace / channel (Slack)
    * status or severity
    * namespace

### Contributing

In case of any bug fixing or improvement, please send pull request.