from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='jwt_')

    secret: str
    algorithm: str
    expire_min: int = 60


AUTH_CONFIG = AuthConfig()
