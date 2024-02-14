from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain_community.chat_models import ChatOllama
from langserve import add_routes

from app import config

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(
    app,
    ChatOllama(
        model=config.OLLAMA_CHAT_MODEL,
        base_url=config.OLLAMA_URL,
    ),
    path="/ollama"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
