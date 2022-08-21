import argparse

from app.common.logger import logger
from app.config.settings import EnvSettings
from app.core.server import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    logger.info(f"ENVIRONMENT={EnvSettings.environment}")

    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
