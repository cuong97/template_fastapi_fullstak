import os

from app.config import config
from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    jwt_private_key: str = "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60
    environment: str = "local"
    api_prefix: str = f"/api"
    title: str = "Template FastApi"
    description: str = "Template fast api"
    version: str = "0.1.0"
    origins: list = ["*"]


class YmlSettings:
    def __init__(self, env):
        self.env = env

    def get_config_env(self):
        base_path = os.getcwd()
        path = f"{base_path}/app/config/config_env.yml"
        yml = config.YMLConfig(
            env=self.env,
            config_file_path=path,
        )
        yml.get_yml_config()
        return yml.yml_config


env_settings = EnvSettings()
setting = YmlSettings(env=env_settings.environment)
