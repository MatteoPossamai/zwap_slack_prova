from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from action.script.email_sender import postmark_template_email_send

from action import client

from rest_framework.views import APIView


class PostmarkTemplateEmail(APIView):  # BaseApiView

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = request.data
        text = data.get('text')

        try:
            postmark_template_id, csv_file_url = int(text.split()[0]), text.split()[1]
        except ValueError:
            client.chat_postMessage(channel='#test', text='Second argument must be an integer')
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST})

        postmark_template_email_send.delay(postmark_template_id, csv_file_url)
        client.chat_postMessage(channel='#test', text='Sending email...')

        return JsonResponse({'data': 'postmark_template_email', 'status': status.HTTP_200_OK})

# /postmark_template_email  28473320 https://drive.google.com/file/d/1OT7Vo2s9QpUCqxziwjFvwOkJSge9jPWg/view?usp=sharing
