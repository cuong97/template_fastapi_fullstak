from app.common.handle_error import APIException
from app.router.v1_router import api_v1_router
from env_settings import env_settings
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """
    Create object FatAPI
    :return:
    """
    app = FastAPI(
        title=env_settings.title,
        description=env_settings.description,
        version=env_settings.version,
    )

    register_cors(app)
    register_router(app)
    register_exception(app)

    @app.on_event("startup")
    async def startup_event():
        pass

    return app


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
