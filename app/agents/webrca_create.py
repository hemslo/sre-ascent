from typing import Any

from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from .util import create_ollama_functions_agent
from ..dependencies.ollama_functions_model import ollama_functions_model
from ..tools.webrca_create import webrca_create

tools = [webrca_create]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            "{input}",
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

webrca_create_agent = create_ollama_functions_agent(
    llm=ollama_functions_model,
    tools=tools,
    prompt=prompt,
)


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: Any


webrca_create_agent_executor = AgentExecutor(
    agent=webrca_create_agent,
    tools=tools,
).with_types(
    input_type=Input,
    output_type=Output,
)
