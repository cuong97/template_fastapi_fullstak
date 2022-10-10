import redis.asyncio as redis
from app.common.constants import TOKEN_USER
from app.common.database import engine
from app.common.handle_error import APIException
from app.models.charger_model import ChargerModel
from app.models.user import User
from app.router.v1_router import api_v1_router
from env_settings import env_settings
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint as req_res
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class FastAPIAdmin(FastAPI):
    async def configure(
        self,
        redis: redis.Redis,
        app: FastAPI,
    ):
        self.redis = redis
        self.app = app
        self.app.add_middleware(
            BaseHTTPMiddleware,
            dispatch=self.verify_authenticate,
        )

    async def verify_authenticate(
        self,
        request: Request,
        call_next: req_res,
    ):
        authorization: str = request.headers.get("Authorization")
        guest: str = request.headers.get("Guest")
        user = None
        if guest and guest.lower() == "guest":
            user = None
        else:
            scheme, param = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "Not authenticated"},
                )
            try:
                token = jwt.decode(
                    param,
                    env_settings.jwt_private_key,
                    algorithms=[env_settings.jwt_algorithm],
                )
            except JWTError:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "Not authenticated"},
                )
            redis = request.app.redis
            if token.get("id"):
                token_key = TOKEN_USER.format(token=token.get("id"))
                user = await redis.get(token_key)
        request.state.user = user
        response = await call_next(request)
        return response


def create_app() -> FastAPI:
    """
    Create object FatAPI
    :return:
    """
    app = FastAPIAdmin(
        title=env_settings.title,
        description=env_settings.description,
        version=env_settings.version,
    )
    create_table()
    register_cors(app)
    register_router(app)
    register_exception(app)

    @app.on_event("startup")
    async def startup():
        r = await redis.from_url(
            env_settings.redis_url,
            decode_responses=True,
            encoding="utf8",
        )
        await app.configure(redis=r, app=app)

    @app.on_event("shutdown")
    async def shutdown_event():
        await app.redis.close()

    return app


def create_table():
    User.__table__.create(engine, checkfirst=True)
    ChargerModel.__table__.create(engine, checkfirst=True)


def register_router(app: FastAPI) -> None:
    """
    Register route
    :param app:
    :return:
    """
    app.include_router(api_v1_router)


def register_cors(app: FastAPI) -> None:
    """
    Register cors
    :param app:
    :return:
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=env_settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception(app: FastAPI) -> None:
    """
    Register exception
    exception_handler
    exception_handlers
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    @app.exception_handler(APIException)
    async def unicorn_exception_handler(exc: APIException):
        return JSONResponse(
            status_code=exc.http_status,
            content={"message": f"{exc.message}"},
        )
