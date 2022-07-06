from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from action import client, SLACK_VERIFICATION_TOKEN

from rest_framework.views import APIView


class Events(APIView):  # BaseApiView

    def post(self, request: Request) -> JsonResponse:
        """
        Description: Base event handler for Slack events
        :param request: Request object with event data
        :return: JsonResponse => Return to Slack a response as a confirmation
        """
        slack_message = request.data

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return JsonResponse({'status': status.HTTP_403_FORBIDDEN})

        # Connection challenge, at first connection
        if slack_message.get('type') == 'url_verification':
            return JsonResponse({'status': status.HTTP_200_OK, 'data': slack_message})

        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # Ignore bots own messages
            if event_message.get('subtype') == 'bot_message':
                return JsonResponse({'status': status.HTTP_200_OK})

            # Get user messages
            user = event_message.get('user')
            text = event_message.get('text')
            if 'hi' in text.lower():
                client.chat_postMessage(channel='#test', text=f'Hi <@{user}> :wave:')
                return JsonResponse({'status': status.HTTP_200_OK})

        return JsonResponse({'status': status.HTTP_200_OK})
