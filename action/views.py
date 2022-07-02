import pandas as pd
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from slack.errors import SlackApiError
from rest_framework.request import Request
import logging
from action.script import query_parser, remote_file_reader

from zwapSlackProva import settings
import slack
import csv
import requests
from io import StringIO

client = slack.WebClient(settings.OAUTH_ACCESS_TOKEN)
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN


class Events(APIView):

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        slack_message = request.data

        # if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
        # return Response(status=status.HTTP_403_FORBIDDEN)

        # For the connection challenge, just return a 200
        if slack_message.get('type') == 'url_verification':
            return JsonResponse({'status': status.HTTP_200_OK, 'data': slack_message})

            # greet bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # ignore bots own message
            if event_message.get('subtype') == 'bot_message':
                return JsonResponse({'status': status.HTTP_200_OK})

            # process user's message
            user = event_message.get('user')
            text = event_message.get('text')
            channel = event_message.get('channel')
            bot_text = 'Hi <@{}> :wave:'.format(user)
            if 'hi' in text.lower():
                client.chat_postMessage(channel='#test', text='Hello world!')
                return JsonResponse({'status': status.HTTP_200_OK})

        return JsonResponse({'status': status.HTTP_200_OK})


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


class PostmarkTemplateEmail(APIView):
    # https://drive.google.com/file/d/1OT7Vo2s9QpUCqxziwjFvwOkJSge9jPWg/view?usp=sharing

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = request.data
        text = data.get('text')

        try:
            postmark_template_id, csv_file_url = int(text.split()[0]), text.split()[1]
        except ValueError:
            client.chat_postMessage(channel='#test', text='Argument must be an integer')

        client.chat_postMessage(channel='#test', text='Sending email...')

        try:
            df = remote_file_reader.read_remote_csv(csv_file_url)

            for item in df.itertuples():
                print(item.email)
                # Send the email
                # ------------------!!!!!!!!!!!!!!!!!!!!!

            # Confirmation of everything went well
            client.chat_postMessage(channel='#test', text="Emails have been sent correctly via PostMark")

        except IndexError:
            client.chat_postMessage(channel='#test', text="Please, provide both the postmark template id and the csv "
                                                          "file path")
        except FileNotFoundError:
            client.chat_postMessage(channel='#test', text="The csv file doesn't exist")
        except SlackApiError as e:
            logging.debug(e.response)
        except ValueError as e:
            client.chat_postMessage(channel='#test', text="The given link may be not valid")

        return JsonResponse({'data': 'postmark_template_email', 'status': status.HTTP_200_OK})


class PostmarkPlainTextEmail(APIView):
    # https://drive.google.com/file/d/1802XAvZ4zfbFdSo_z_-eDULirBjvOqrH/view?usp=sharing

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = request.data
        text = data.get('text')

        html_template_url, csv_file_url = text.split()[0], text.split()[1]

        client.chat_postMessage(channel='#test', text='Sending email...')

        try:
            df = remote_file_reader.read_remote_csv(csv_file_url)
            template = remote_file_reader.read_remote_html(html_template_url)

            for item in df.itertuples():
                pass
                # Send the email
                # ------------------!!!!!!!!!!!!!!!!!!!!!

            # Confirmation of everything went well
            client.chat_postMessage(channel='#test', text="Emails have been sent correctly via PostMark")

        except IndexError:
            client.chat_postMessage(channel='#test', text="Please, provide both the postmark template id and the csv "
                                                          "file path")
        except FileNotFoundError:
            client.chat_postMessage(channel='#test', text="The csv file doesn't exist")
        except SlackApiError as e:
            logging.debug(e.response)
        except ValueError as e:
            client.chat_postMessage(channel='#test', text=f"The given link may be not valid \n {e}")

        return JsonResponse({'data': 'postmark_plain_text_email', 'status': status.HTTP_200_OK})


class QueryUsers(APIView):

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        # Get the text from the request
        data = request.data
        text = data.get('text')
        print('Arrived to the query users view')

        if len(text) == 0:
            client.chat_postMessage(channel='#test', text="Please, provide the query")

        else:
            # Create what needed to perform query
            query = text.split()

            client.chat_postMessage(channel='#test', text='Query check and perform is started')

            # Check if the query is valid
            valid, explaination = query_parser.query_checker(query)

            print(valid, explaination)

            if valid and False:
                # Perform the query
                result = query_parser.query_executor(query)

                # Send the result to the channel
                client.chat_postMessage(channel='#test', text=result)
            else:
                client.chat_postMessage(channel='#test', text=f'Error:{explaination}')

        return JsonResponse({'data': 'query_user', 'status': status.HTTP_200_OK, 'text': text})


class LinkNFC(APIView):

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        # Get the user

        # Query the db to get the user's NFC
        # ----------------------------------------------------

        result = 'X'
        client.chat_postMessage(channel='#test', text='Link NFC of given user is the following:')
        client.chat_postMessage(channel='#test', text=f'https://zwap.in/profile?card={result}')

        return JsonResponse({'data': 'query_user', 'status': status.HTTP_200_OK})
