from app.schemas.response import resp
from fastapi.routing import APIRouter

router_index = APIRouter()


@router_index.get("/")
async def index():
    return resp.success(data="Hello World")
