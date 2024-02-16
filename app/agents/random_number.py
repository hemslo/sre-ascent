from typing import Any

from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from .util import create_ollama_functions_agent
from ..dependencies.ollama_functions_model import ollama_functions_model
from ..tools.random_number import random_number

tools = [random_number]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            "{input}",
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

random_number_agent = create_ollama_functions_agent(
    llm=ollama_functions_model,
    tools=tools,
    prompt=prompt,
)


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: Any


random_number_agent_executor = AgentExecutor(
    agent=random_number_agent,
    tools=tools,
).with_types(
    input_type=Input,
    output_type=Output,
)
