from backend.app.config import settings
from backend.tests.base_test import BaseTestCase
from backend.tests.factories.charger_model import ChargerModelFactory


class TestChargerModel(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        ChargerModelFactory.create()

    def test_list(self):
        response = self.client.get(f"{settings.EnvSettings.api_prefix}/charger-models")
        res = response.json()
        assert response.status_code == 200
        assert len(res["data"]) == 1
        assert res["msg"] == "success"
