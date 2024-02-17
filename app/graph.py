import functools
import operator
from collections.abc import Mapping
from typing import Annotated, Sequence, TypedDict

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, FunctionMessage, ChatMessage, \
    ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.pregel import Pregel
from pydantic import BaseModel

from app.chains.supervisor import build_supervisor_chain
from app.dependencies.openai_chat_model import openai_chat_model
from app.tools.datetime_provider import datetime_provider
from app.tools.random_number import random_number
from app.tools.random_select import random_select
from app.tools.slack_toolkit import slack_toolkit
from app.tools.webrca_create import webrca_create
from app.tools.duckduckgo_search import duckduckgo_search
from app.tools.slack_searcher import slack_searcher


# https://github.com/langchain-ai/langgraph/blob/main/examples/multi_agent/agent_supervisor.ipynb

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


SUPERVISOR_NAME = "Supervisor"

GRAPH = {
    "RandomNumber": {
        "tools": [random_number],
        "system_prompt": "You are a random number generator.",
    },
    "RandomSelect": {
        "tools": [random_select],
        "system_prompt": "You are a random selector.",
    },
    "WebrcaCreate": {
        "tools": [webrca_create],
        "system_prompt": "You are a webrca incident creator.",
    },
    "GenericSearch": {
        "tools": [duckduckgo_search],
        "system_prompt": "You are a search engine for generic questions.",
    },
    "SlackToolkit": {
        "tools": slack_toolkit.get_tools(),
        "system_prompt": "You are a slack toolkit.",
    },
    "SlackSearcher": {
        "tools": [slack_searcher],
        "system_prompt": "You are a slack searcher.",
    },
    "DatetimeProvider": {
        "tools": [datetime_provider],
        "system_prompt": "You are a datetime provider.",
    },
}

SUPERVISOR_MEMBERS = {k: v["system_prompt"] for k, v in GRAPH.items()}


def build_graph() -> Pregel:
    supervisor_chain = build_supervisor_chain(SUPERVISOR_MEMBERS)

    workflow = StateGraph(AgentState)
    for member, config in GRAPH.items():
        agent = create_agent(openai_chat_model, config["tools"], config["system_prompt"])
        workflow.add_node(member, functools.partial(agent_node, agent=agent, name=member))
    workflow.add_node(SUPERVISOR_NAME, supervisor_chain)

    for member in GRAPH:
        workflow.add_edge(member, SUPERVISOR_NAME)

    conditional_map = {k: k for k in GRAPH} | {"FINISH": END}
    workflow.add_conditional_edges(SUPERVISOR_NAME, lambda x: x["next"], conditional_map)
    workflow.set_entry_point(SUPERVISOR_NAME)

    return workflow.compile()


class Input(BaseModel):
    messages: Sequence[HumanMessage | AIMessage | SystemMessage | FunctionMessage | ChatMessage | ToolMessage]
    next: str | None


graph = build_graph().with_types(input_type=Input)
