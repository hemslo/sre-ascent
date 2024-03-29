import json
from typing import Annotated

from fastapi import Depends
from langchain_core.messages import HumanMessage
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import config
from app.graph import graph

app = App(
    token=config.SLACK_BOT_TOKEN,
    signing_secret=config.SLACK_SIGNING_SECRET
)

slack_request_handler = SlackRequestHandler(app)

slack_socket_model_handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)


def get_slack_request_handler() -> SlackRequestHandler:
    return slack_request_handler


SlackRequestHandlerDep = Annotated[SlackRequestHandler, Depends(get_slack_request_handler)]


def invoke_graph(body) -> str:
    payload = {
        "text": body["event"].get("text"),
        "channel": body["event"].get("channel"),
        "ts": body["event"].get("ts"),
        "thread_ts": body["event"].get("thread_ts"),
    }
    response = graph.invoke({
        "messages": [HumanMessage(content=json.dumps(payload))],
    })
    return "\n".join(message.content for message in response["messages"][1:])


@app.event("message")
def handle_message_events(body, say, logger):
    if body.get('event', {}).get('channel_type') != 'im':
        return
    logger.info(body)
    response = invoke_graph(body)
    say(response, thread_ts=body['event']['ts'])


# Define an event listener for "app_mention" events
@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    logger.info(body)
    response = invoke_graph(body)
    say(response, thread_ts=body['event']['ts'])
