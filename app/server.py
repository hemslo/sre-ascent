from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from app.agents.random_number import random_number_agent_executor
from app.agents.search_agent import search_engine_agent_executor
from app.agents.thread_summary import thread_summary_agent_executor
from app.chains.extraction import extraction_chain
from app.chains.supervisor import build_supervisor_chain
from app.agents.webrca_create import webrca_create_agent_executor
from app.dependencies.ollama_chat_model import ollama_chat_model
from app.graph import graph, SUPERVISOR_MEMBERS
from app.routers import slack

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(
    app,
    ollama_chat_model,
    path="/ollama"
)

add_routes(
    app,
    extraction_chain,
    path="/extraction",
)

add_routes(
    app,
    random_number_agent_executor,
    path="/random_number",
)

add_routes(
    app,
    webrca_create_agent_executor,
    path="/webrca_create",
)

add_routes(
    app,
    search_engine_agent_executor,
    path="/generic",
)

add_routes(
    app,
    thread_summary_agent_executor,
    path="/thread_summary",
)

add_routes(
    app,
    build_supervisor_chain(SUPERVISOR_MEMBERS),
    path="/supervisor",
)

add_routes(
    app,
    graph,
    path="/graph",
)

app.include_router(slack.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
