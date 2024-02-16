from typing import Any

from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from .util import create_ollama_functions_agent
from ..dependencies.ollama_functions_model import ollama_functions_model
from ..tools.slack_searcher import slack_searcher

tools = [slack_searcher]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            "{input}",
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

slack_searcher_agent = create_ollama_functions_agent(
    llm=ollama_functions_model,
    tools=tools,
    prompt=prompt,
)


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: Any

slack_searcher_agent_executor = AgentExecutor(
    agent=slack_searcher_agent,
    tools=tools,
).with_types(
    input_type=Input,
    output_type=Output,
)
