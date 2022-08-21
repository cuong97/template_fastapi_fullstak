from unittest import TestCase

from app.common import database
from app.config.settings import yml_setting
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions

yml_setting.env = "local_test"
env_yml = yml_setting.get_config_env()
engine_test = create_engine(env_yml.get("DB_URL"))
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def _get_test_db():
    try:
        yield SessionTest()
    finally:
        pass


class BaseTestCase(TestCase):
    app.dependency_overrides[database.get_db] = _get_test_db
    client = TestClient(app)
    api_prefix = "/api"

    def setUp(self):
        database.DBBaseCustom.metadata.create_all(bind=engine_test)

    def tearDown(self):
        close_all_sessions()
        database.DBBaseCustom.metadata.drop_all(engine_test)
