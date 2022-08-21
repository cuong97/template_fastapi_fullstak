from app.common.logger import logger
from app.core.server import create_app
from env_settings import env_settings

app = create_app()

if __name__ == "__main__":
    import uvicorn

    logger.info(f"ENVIRONMENT={env_settings.environment}")

    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
