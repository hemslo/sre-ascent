import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.fastapi import SlackRequestHandler
from fastapi import FastAPI, Request

# Initialize a Bolt for sre-ascent-dev app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Define an event listener for "message" events
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

# FastAPI app to handle routes
fastapi_app = FastAPI()

# Create a request handler for the app
handler = SlackRequestHandler(app)

@fastapi_app.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)

# Check if the script is being run directly
if __name__ == "__main__":
    # Check if SLACK_APP_TOKEN is set for Socket Mode
    if 'SLACK_APP_TOKEN' in os.environ:
        # Start the app in Socket Mode
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        handler.start()
    else:
        # If not using socket mode, we can start the FastAPI app using the command in terminal:
        # uvicorn app:fastapi_app --reload --port 3000
        print("SLACK_APP_TOKEN not found. Please set it to run in Socket Mode or to run the FastAPI app with uvicorn from the terminal.")
