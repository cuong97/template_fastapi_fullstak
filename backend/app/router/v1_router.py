from fastapi import APIRouter

from backend.app.api.v1.auth_router import auth_router
from backend.app.api.v1.charger_model_router import charger_model_router
from backend.app.api.v1.index import router_index
from backend.app.api.v1.user_router import user_router
from backend.app.api.v1.vehicle_model_router import vehicle_model
from backend.app.config import settings

api_v1_router = APIRouter()

# router index
api_v1_router.include_router(router_index, prefix=f"{settings.API_PREFIX}")

# router charger model
api_v1_router.include_router(
    charger_model_router, prefix=f"{settings.API_PREFIX}/charger-model"
)

# router vehicle model

api_v1_router.include_router(
    auth_router,
    prefix=f"{settings.API_PREFIX}/authentication",
)

api_v1_router.include_router(
    user_router,
    prefix=f"{settings.API_PREFIX}/current_user",
)
api_v1_router.include_router(
    user_router,
    prefix=f"{settings.API_PREFIX}/user",
)
