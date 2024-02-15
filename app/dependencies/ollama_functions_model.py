from langchain_experimental.llms.ollama_functions import OllamaFunctions

from .ollama_chat_model import ollama_chat_model

system_template = """\
You have access to the following tools:

{tools}

You must always select only one of the above tools and respond with only a JSON object matching the following schema:

{{
  "tool": <name of the selected tool>,
  "tool_input": <parameters for the selected tool, matching the tool's JSON schema>
}}

If there is a result from the tool, select `__conversational_response` as the next tool.
"""

ollama_functions_model = OllamaFunctions(
    llm=ollama_chat_model,
    tool_system_prompt_template=system_template,
)
