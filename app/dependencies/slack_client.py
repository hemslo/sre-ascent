from slack_sdk import WebClient

from app import config

slack_bot_client = WebClient(token=config.SLACK_BOT_TOKEN)

slack_user_client = WebClient(token=config.SLACK_USER_TOKEN)
