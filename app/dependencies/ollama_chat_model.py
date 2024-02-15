from langchain_community.chat_models import ChatOllama

from app import config

ollama_chat_model = ChatOllama(
    model=config.OLLAMA_CHAT_MODEL,
    base_url=config.OLLAMA_URL,
    temperature=0,
)
