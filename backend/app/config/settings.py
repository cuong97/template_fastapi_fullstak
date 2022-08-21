import os

from app.config import config
from env_settings import env_settings


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


yml_setting = YmlSettings(env=env_settings.environment)
