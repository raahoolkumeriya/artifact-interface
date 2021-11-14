import os
import logging
from slack import WebClient
from slack.errors import SlackApiError
logging.basicConfig(level=logging.INFO)
from interface.utilities.load_config import SlackConfig


class SlackConnect():
    """
    Slack Message post after artifact creation and successful testing
    """
    def __init__(self, slack_config: SlackConfig):
        """
        Constructor for SlackConnect

        :param slack_config: Configuration setup for slack
        """
        self.slack_config = slack_config
        self.slack_token = os.environ[self.slack_config.authtoken]
        self.client = WebClient(token=self.slack_token)

    def post_in_channel(self, artifact: str, version: str, jira_ticket: str):
        """
        {'ok': True, 'channel': 'CPDSD2B4N', 'ts': '1626890806.001200',
        'message': {'type': 'message', 'subtype': 'bot_message',
        'text': "This content can't be displayed.", 'ts': '1626890806.001200',
        'username': 'codelockerBot', 'bot_id': 'BRC8X0280', 'blocks':
        [{'type': 'section', 'block_id': 'xRdHA', 'text': {'type': 'mrkdwn',
        'text':
        '<https://codelocked.atlassian.net/browse/CODELOCKED-14|[CODELOCKED-14]>
        | *Deployment Package Details:*', 'verbatim': False}},
        {'type': 'divider', 'block_id': 'gvRI'},
        {'type': 'section', 'block_id': 'WzNh4', 'fields': [{'type': 'mrkdwn',
        'text': '*Artifact Name:
        *\nDEPLOYME-10.0.0.1.tar.gz\nDEPLOYME-10.0.0.2.tar.gz\nDEPLOYME-10.0.0.3.tar.gz',
        'verbatim': False},
        {'type': 'mrkdwn', 'text':
        '*Version Name:*\n10.0.0.2', 'verbatim': False}]}]}}
        """
        try:
            response = self.client.chat_postMessage(
                channel=self.slack_config.channelid,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "<https://codelocked.atlassian.net/browse/" + jira_ticket + "|[" + jira_ticket + "]> | *Deployment Package Details:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Artifact Name:*\n" + artifact
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Version Name:*\n" + version
                            }
                        ]
                    }
                ]
            )
            return response.get('ok')
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]
