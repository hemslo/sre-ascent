from slack_sdk import WebClient

from app import config

slack_client = WebClient(token=config.SLACK_BOT_TOKEN)
