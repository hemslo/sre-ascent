from langchain_openai import ChatOpenAI

from app import config

openai_chat_model = ChatOpenAI(
    model_name=config.OPENAI_CHAT_MODEL,
    temperature=0,
)
