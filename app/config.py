import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama2")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
