"""
slack_event_adapter = SlackEventAdapter(settings.SIGNING_SECRET, "/slack/events")
slack_client = slack.WebClient(token=settings.OAUTH_ACCESS_TOKEN)

BOT_ID = slack_client.api_call("auth.test")["user_id"]

@slack_event_adapter.on("message")
def handle_message(payload):
    event = payload.get("event", {})  # give info about what happened
    channel = event.get("channel")
    user = event.get("user")
    text = event.get("text")
    if user != BOT_ID:
        slack_client.chat_postMessage(channel=channel, text=f"You said {text}")
    return "Message received"
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from zwapSlackProva import settings
import slack

client = slack.WebClient(settings.OAUTH_ACCESS_TOKEN)
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN


class Events(APIView):

    def post(self, request, *args, **kwargs):

        slack_message = request.data
        print(slack_message.get('token'), SLACK_VERIFICATION_TOKEN)
        print(slack_message)

        # if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
        # return Response(status=status.HTTP_403_FORBIDDEN)

        # For the connection challenge, just return a 200
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

            # greet bot
        if 'event' in slack_message:
            print(slack_message.get('event'))
            event_message = slack_message.get('event')

            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            # process user's message
            user = event_message.get('user')
            text = event_message.get('text')
            channel = event_message.get('channel')
            bot_text = 'Hi <@{}> :wave:'.format(user)
            if 'hi' in text.lower():
                client.chat_postMessage(channel='#test', text='Hello world!')
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
