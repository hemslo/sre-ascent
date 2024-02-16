from collections.abc import Sequence
from typing import List

from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage, FunctionMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_experimental.llms.ollama_functions import DEFAULT_RESPONSE_FUNCTION


def create_ollama_functions_agent(
    llm: BaseLanguageModel, tools: Sequence[BaseTool], prompt: ChatPromptTemplate
) -> Runnable:
    """
    Patch create_openai_functions_agent to work with ollama
    """
    if "agent_scratchpad" not in prompt.input_variables:
        raise ValueError(
            "Prompt must have input variable `agent_scratchpad`, but wasn't found. "
            f"Found {prompt.input_variables} instead."
        )
    llm_with_tools = llm.bind(
        functions=[DEFAULT_RESPONSE_FUNCTION] + [convert_to_openai_function(t) for t in tools],
        format="json",
    )

    def agent_scratchpad(x):
        return adapt_to_ollama_messages(format_to_openai_function_messages(x["intermediate_steps"]))

    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=agent_scratchpad,
        )
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    return agent


def _map_message(message: BaseMessage) -> BaseMessage:
    if isinstance(message, FunctionMessage):
        return HumanMessage(
            content=f"tool {message.name} result: {message.content}",
        )
    return message


def adapt_to_ollama_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    return [_map_message(m) for m in messages]
