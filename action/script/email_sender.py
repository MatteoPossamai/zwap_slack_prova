import logging
from typing import Tuple, Any

from email_client_api import PostmarkApi
from slack.errors import SlackApiError

from action import client
from action.script import read_remote_csv
from celery import shared_task


@shared_task
def postmark_template_email_send(postmark_template_id: int, csv_file_url: str) -> None:
    print('OK')
    try:
        df = read_remote_csv(csv_file_url)
        postmark_session = PostmarkApi(server_token='de1408cd-a60b-4716-aa4c-1a2de7183524',
                                       email_from='hello@zwap.in')

        for item in df.itertuples():
            if isinstance(item.email, str):
                template_vars = item._asdict()

                email_template_data = postmark_session.prepare_batch_template(item.email, postmark_template_id,
                                                                              template_vars)
                print(email_template_data)
                email_status = postmark_session.send_template_email(email_template_data)

                if email_status.error_code != 0:
                    client.chat_postMessage(channel='#test', text=f'Error sending email to {item.email}')

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
