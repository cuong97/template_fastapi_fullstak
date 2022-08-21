from fastapi import APIRouter

from backend.app.api.v1.auth_router import auth_router
from backend.app.api.v1.charger_model_router import charger_model_router
from backend.app.api.v1.index import router_index
from backend.app.api.v1.user_router import user_router
from backend.app.config import settings

api_v1_router = APIRouter()

# router index
api_v1_router.include_router(router_index, prefix=f"{settings.EnvSettings.api_prefix}")

# router charger model
api_v1_router.include_router(
    charger_model_router, prefix=f"{settings.EnvSettings.api_prefix}/charger-model"
)

api_v1_router.include_router(
    auth_router,
    prefix=f"{settings.EnvSettings.api_prefix}/authentication",
)

api_v1_router.include_router(
    user_router,
    prefix=f"{settings.EnvSettings.api_prefix}/user",
)
