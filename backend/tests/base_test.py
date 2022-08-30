from unittest import TestCase

from app.common import database
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm.session import close_all_sessions


class BaseTestCase(TestCase):
    client = TestClient(app)
    api_prefix = "/api"

    def setUp(self):
        database.DBBaseCustom.metadata.create_all(bind=database.engine)

    def tearDown(self):
        close_all_sessions()
        database.DBBaseCustom.metadata.drop_all(database.engine)
