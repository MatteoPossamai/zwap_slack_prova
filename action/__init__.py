import slack
from zwapSlackProva import settings

client = slack.WebClient(settings.OAUTH_ACCESS_TOKEN)
SLACK_VERIFICATION_TOKEN = settings.SLACK_VERIFICATION_TOKEN
