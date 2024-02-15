from langchain_community.llms import Ollama
from langchain.tools import DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent, create_openai_functions_agent
from langchain_community.chat_models import ChatOpenAI

#prompt = hub.pull("hwchase17/react-chat-json")
prompt = hub.pull("hwchase17/openai-functions-agent")
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
ddg_tool = DuckDuckGoSearchRun(max_results=1)
tools = [ddg_tool, wiki_tool]
llm=Ollama(model="llama2")
llm.invoke("what is the weather in Auckland today?")
'''
agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

agent_executor.invoke({"input":"what is the weather in Auckland today?"})
'''

