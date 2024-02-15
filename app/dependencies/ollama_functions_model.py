from langchain_experimental.llms.ollama_functions import OllamaFunctions, DEFAULT_SYSTEM_TEMPLATE

from .ollama_chat_model import ollama_chat_model

ollama_functions_model = OllamaFunctions(
    llm=ollama_chat_model,
    tool_system_prompt_template=DEFAULT_SYSTEM_TEMPLATE,
)
