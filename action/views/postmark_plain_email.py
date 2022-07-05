import logging

from django.http import JsonResponse
from email_client_api import PostmarkApi
from rest_framework import status
from rest_framework.views import APIView
from slack.errors import SlackApiError
from rest_framework.request import Request

from action import client
from action.script import insert_params_into_html, read_remote_html, read_remote_csv


class PostmarkPlainTextEmail(APIView): # BaseApiView
    # https://drive.google.com/file/d/1U3yqeWV3tq2bwxrScFPjI2N1ljJCnG0K/view?usp=sharing

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        data = request.data
        text = data.get('text')

        html_template_url, csv_file_url = text.split()[0], text.split()[1]

        client.chat_postMessage(channel='#test', text='Sending email...')

        try:
            df = read_remote_csv(csv_file_url)
            template = read_remote_html(html_template_url)

            postmark_session = PostmarkApi(server_token='de1408cd-a60b-4716-aa4c-1a2de7183524',
                                           email_from='matteo@zwap.in')

            for item in df.itertuples():
                if isinstance(item.email, str):
                    template_vars = item._asdict()
                    html = insert_params_into_html(template, item, template_vars)
                    print(html, template_vars)

                    """

                    email_template_data = postmark_session.prepare_batch_plain_text(item.email)
                    email_status = postmark_session.send_template_email(email_template_data)

                    if email_status.error_code != 0:
                        client.chat_postMessage(channel='#test', text=f'Error sending email to {item.email}')

                    """

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