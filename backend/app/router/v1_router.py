from app.api.v1.auth_router import auth_router
from app.api.v1.charger_model_router import charger_model_router
from app.api.v1.index import router_index
from app.api.v1.user_router import user_router
from app.config import settings
from fastapi import APIRouter

api_v1_router = APIRouter()

# router index
api_v1_router.include_router(router_index)

# router charger model
api_v1_router.include_router(
    charger_model_router, prefix=f"{settings.env_settings.api_prefix}/charger-model"
)

api_v1_router.include_router(
    auth_router,
    prefix=f"{settings.env_settings.api_prefix}/authentication",
)

api_v1_router.include_router(
    user_router,
    prefix=f"{settings.env_settings.api_prefix}/user",
)
