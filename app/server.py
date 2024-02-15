from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from app.chains.extraction import extraction_chain
from .dependencies.ollama_chat_model import ollama_chat_model

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
