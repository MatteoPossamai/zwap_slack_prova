import logging

import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from slack.errors import SlackApiError

from action import client

from rest_framework.views import APIView


class TopZwappers(APIView):

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = request.data
        text = data.get('text')

        try:
            # Get the number of zwappers, according to the text or the default value
            number = 10 if len(text) == 0 else int(text.split()[0])

            # --------------------------------------------------
            # Query on the db to retrieve the top zwappers
            # ----------------------------------------------------

            # Get the top zwappers
            df = pd.DataFrame([
                ['a@b.com', 10],
                ['a@b.com', 10],
                ['a@b.com', 10],
                ['a@b.com', 10],
                ['a@b.com', 10],
                ['a@b.com', 10],
            ], columns=['EMAIL', 'SUBSCRIPTION'])

            # Writing down on the csv file
            df.to_csv('templates/zwappers.csv')

            # Sending the csv file to the channel
            client.chat_postMessage(channels='#test', text=f'Here are the {number} top zwappers:')
            client.files_upload(channels='#test', file='templates/zwappers.csv')

        except SlackApiError as e:
            logging.debug(e)
        except ValueError:
            client.chat_postMessage(channel='#test', text='Argument must be an integer')

        return JsonResponse({'data': 'top_zwappers', 'status': status.HTTP_200_OK})
