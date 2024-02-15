from typing import Annotated

from fastapi import Depends
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import config

app = App(
    token=config.SLACK_BOT_TOKEN,
    signing_secret=config.SLACK_SIGNING_SECRET
)

slack_request_handler = SlackRequestHandler(app)

slack_socket_model_handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)


def get_slack_request_handler() -> SlackRequestHandler:
    return slack_request_handler


SlackRequestHandlerDep = Annotated[SlackRequestHandler, Depends(get_slack_request_handler)]

@app.event("message")
def handle_message_events(body, say, logger):
    logger.info(body)
    text = body.get('event', {}).get('text', '')
    if 'hello' in text.lower():
        say("Hello there! :wave:")


# Define an event listener for "app_mention" events
@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    logger.info(body)
    say("Hello SRE slackers! :blush:")
