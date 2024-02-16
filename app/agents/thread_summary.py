from typing import Any

from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

from .util import create_ollama_functions_agent
from ..dependencies.ollama_functions_model import ollama_functions_model
from ..tools.get_thread_msg import get_thread_msg

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

class Input(BaseModel):
    input: str
    thread_ts: str

class Output(BaseModel):
    output: Any

# Define the tool for this agent
tools = [get_thread_msg]
llm = ollama_functions_model

# Create the agent
agent = create_ollama_functions_agent(llm, tools, prompt)

thread_summary_agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
).with_types(
    input_type=Input,
    output_type=Output,
)

