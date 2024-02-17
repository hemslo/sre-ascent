from langchain_core.tools import tool
from slack_sdk.errors import SlackApiError

from app.dependencies.slack_client import slack_client


@tool()
def get_thread_msg(channel_id: str, thread_ts: str):
    """
    Retrieves messages from a specified thread.
    """
    try:
        response = slack_client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = response['messages']
        return {'thread_messages': messages}
    except SlackApiError as e:
        print(f"Error fetching thread messages: {e}")
        return {'error': str(e)}
