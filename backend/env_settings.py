from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    jwt_private_key: str = "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60
    environment: str = "local"
    api_prefix: str = "/api"
    title: str = "Template FastApi"
    description: str = "Template fast api"
    version: str = "0.1.0"
    origins: list = ["*"]
    redis_url: str = "redis://localhost:6379"


env_settings = EnvSettings()
