from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='rabbitmq_')

    host: str
    port: int
    user: str
    password: str
    vhost: str

    @cached_property
    def connection_url(self) -> str:
        return f'amqp://{self.user}:{self.password}@{self.host}:{self.port}//{self.vhost}'


RABBITMQ_CONFIG = RabbitMQConfig()
