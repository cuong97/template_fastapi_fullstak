from unittest import TestCase

from app.common.database import DBBaseCustom, get_db
from app.config import settings
from app.config.settings import setting
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions

setting.env = "local_test"
env_yml = setting.get_config_env()
engine_test = create_engine(env_yml.get("DB_URL"))
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def _get_test_db():
    try:
        yield SessionTest()
    finally:
        pass


class BaseTestCase(TestCase):
    app.dependency_overrides[get_db] = _get_test_db
    client = TestClient(app)
    api_prefix = settings.EnvSettings.api_prefix

    def setUp(self):
        DBBaseCustom.metadata.create_all(bind=engine_test)

    def tearDown(self):
        close_all_sessions()
        DBBaseCustom.metadata.drop_all(engine_test)
