import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from app import config

load_dotenv()

# Initialize a Slack WebClient instance
slack_client = WebClient(token=config.SLACK_BOT_TOKEN)

def list_accessible_channels():
    try:
        # Call the conversations.list method to fetch a list of channels
        response = slack_client.conversations_list(types="public_channel,private_channel")
        
        # Check if the API call was successful
        if response["ok"]:
            channels = response["channels"]
            channel_info = {channel["id"]: channel["name"] for channel in channels}
            return channel_info
        
        else:
            # print(f"Error: {response['error']}")
            return {}

    except SlackApiError as e:
        # print(f"Error: {e.response['error']}")
        return {}

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
                return "@"+profile["display_name"]
            else:
                return user_id
        
        else:            
            # print(f"Error: {response['error']}")
            return None

    except SlackApiError as e:
        # print(f"Error: {e.response['error']}")
        return None

def search_in_channel(channel_id, channel_name, keyword):
    found_messages = []
    try:
        # Call the conversations.history method to fetch messages from a channel
        response = slack_client.conversations_history(channel=channel_id)
        
        # Check if the API call was successful
        if response["ok"]:
            messages = response["messages"]
            
            # Iterate through each message and check for the keyword
            for message in messages:
                if "text" in message:
                    text = message["text"]
                    # Replace user IDs with human-readable names
                    for user_id in re.findall(r"<@(\w+)>", text):
                        user_name = get_user_name(user_id)
                        if user_name:
                            text = text.replace(f"<@{user_id}>", user_name)
                    if keyword in text:
                        found_messages.append((channel_name, text))
        
        # else:
            # print(f"Error: {response['error']}")

    except SlackApiError as e:
        # print(f"Error: {e.response['error']}")
        return found_messages
    
    return found_messages

def search_in_channels(channels, channel_info, keyword):
    found_messages = []
    # Iterate through each channel and search for the keyword
    for channel_id, channel_name in channel_info.items():
        # print(f"Searching for '{keyword}' in channel: {channel_name} ({channel_id})")
        messages_in_channel = search_in_channel(channel_id, channel_name, keyword)
        found_messages.extend(messages_in_channel)
    return found_messages

def slack_searcher(keyword):
    # List all accessible channels
    accessible_channels = list_accessible_channels()
    
    if accessible_channels:
        # print("Accessible Channels:")
        # for channel_id, channel_name in accessible_channels.items():
            # print(f"{channel_name} ({channel_id})")
        
        # Search for the keyword in the accessible channels
        found_messages = search_in_channels(accessible_channels, accessible_channels, keyword)

        return found_messages
    else:
        # print("No accessible channels found.")
        return []

# if __name__ == "__main__":
#     import re
    
#     search_keyword = "testing"
#     found_messages = search_all_channels(search_keyword)
    
#     if found_messages:
#         print("\nFound messages:")
#         for channel_name, message_text in found_messages:
#             print(f"In {channel_name}: {message_text}")
#     else:
#         print("No messages found matching the keyword.")
