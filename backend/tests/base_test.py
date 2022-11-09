from unittest import TestCase

from app.common import database
from fastapi.testclient import TestClient

from app.common.database import engine
from app.models.charger_model import ChargerModel
from app.models.items import Item
from app.models.user import User
from main import app
from sqlalchemy.orm.session import close_all_sessions


class BaseTestCase(TestCase):
    client = TestClient(app)
    api_prefix = "/api"

    def setUp(self):
        User.__table__.create(engine, checkfirst=True)
        ChargerModel.__table__.create(engine, checkfirst=True)
        Item.__table__.create(engine, checkfirst=True)

    def tearDown(self):
        close_all_sessions()
        database.DBBaseCustom.metadata.drop_all(database.engine)
