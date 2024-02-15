from fastapi import APIRouter, Request

from app.dependencies.slack import SlackRequestHandlerDep

router = APIRouter()


@router.post("/slack/events")
async def slack_events(request: Request, handler: SlackRequestHandlerDep):
    return await handler.handle(request)
