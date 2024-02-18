import re
from slack_sdk.errors import SlackApiError
from langchain_core.tools import tool
from app.dependencies.slack_client import slack_client


def get_user_name(user_id):
    try:
        # Call the users.info method to fetch user information
        response = slack_client.users_info(user=user_id)

        # Check if the API call was successful
        if response["ok"]:
            user_info = response["user"]
            profile = user_info["profile"]
            # print(user_info)
            if "display_name" in profile:
                return "@" + profile["display_name"]
            else:
                return user_id

        else:
            return None

    except SlackApiError:
        return None


def search_messages(keyword):
    try:
        # Call the search.messages method to search for messages containing the keyword
        response = slack_client.search_messages(query=keyword)
        
        # Check if the API call was successful
        if response["ok"]:
            messages = response["messages"]["matches"]
            found_messages = []
            
            # Iterate through each message and extract relevant information
            for message in messages:
                channel_id = message["channel"]["id"]
                channel_name = message["channel"]["name"]
                text = message["text"]

                # Replace user IDs with human-readable names
                for user_id in re.findall(r"<@(\w+)>", text):
                    user_name = get_user_name(user_id)
                    if user_name:
                        text = text.replace(f"<@{user_id}>", user_name)
                found_messages.append((channel_name, text))
            
            return found_messages
        
        else:
            # print(f"Error: {response['error']}")
            return []

    except SlackApiError as e:
        print(f"Error: {e.response['error']}")
        return []

@tool()
def slack_searcher(keyword: str) -> list[tuple[str, str]]:
    """
    Search slack for the keyword
    """
    found_messages = search_messages(keyword)

    if found_messages:
        # for channel_name, message_text in found_messages:
        #     print(f"In {channel_name}: {message_text}")
        return found_messages
    else:
        return []