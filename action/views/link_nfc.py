from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request

from action import client


class LinkNFC(APIView):  # BaseApiView

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        # Get the user
        data = request.data
        text = data.get('text')
        try:
            email = text.split()[0]
        except IndexError:
            client.chat_postMessage(channel='#test', text="Please, provide the user email")

        # Query the db to get the user's NFC
        # ZwapUserModel.objects.filter(email=email).values('card_code')

        if True:  # query.exists():
            result = 'X'
            client.chat_postMessage(channel='#test', text='Link NFC of given user is the following:')
            client.chat_postMessage(channel='#test', text=f'https://zwap.in/profile?card={result}')
        else:
            client.chat_postMessage(channel='#test', text='User not found')

        return JsonResponse({'data': 'query_user', 'status': status.HTTP_200_OK})