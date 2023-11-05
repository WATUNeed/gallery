from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class DbConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='db_')

    user: str
    host: str
    port: str
    name: str
    driver: str
    password: str
    ddl_show: bool = False

    @cached_property
    def connection_url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


DB_CONFIG = DbConfig()
