import json

from app.common.constants import TOKEN_USER
from app.schemas.response import resp
from fastapi.routing import APIRouter
from starlette.requests import Request

router_index = APIRouter()


@router_index.get("/")
async def index(request: Request):
    if request.state.user:
        user_id = json.loads(request.state.user).get("id")
        token_key = TOKEN_USER.format(token=user_id)
        await request.app.redis.delete(token_key)
    return resp.success(data="Hello World")
