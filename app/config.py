import os

from dotenv import load_dotenv
from langchain.globals import set_debug, set_verbose

load_dotenv()

DEBUG = os.getenv("DEBUG", "0") == "1"
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "mistral")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
VERBOSE = os.getenv("VERBOSE", "0") == "1"

set_debug(DEBUG)
set_verbose(VERBOSE)
