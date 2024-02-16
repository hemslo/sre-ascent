from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.globals import set_debug
from .util import create_ollama_functions_agent
from ..dependencies.ollama_functions_model import ollama_functions_model
from ..tools.duckduckgo_search import duckduckgo_search
from typing import Any
from pydantic import BaseModel

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            "{input}",
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: Any

tools = [duckduckgo_search]
llm = ollama_functions_model
agent = create_ollama_functions_agent(llm, tools, prompt)

search_engine_agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
).with_types(
    input_type=Input,
    output_type=Output,
)
#text = "What's the weather in Auckland Today"
#messages = [HumanMessage(content=text)]

#search_engine_agent_executor.invoke({"input": text})
