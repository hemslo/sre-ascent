from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from langchain_core.tools import tool
import os

@tool()
def get_thread_msg(channel_id: str, thread_ts: str):
    """
    Retrieves messages from a specified thread.
    """
    client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
    try:
        response = client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = response['messages']
        return {'thread_messages': messages}
    except SlackApiError as e:
        print(f"Error fetching thread messages: {e}")
        return {'error': str(e)}
