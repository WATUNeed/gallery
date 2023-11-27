from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='redis_')

    host: str
    port: int
    driver: str
    user: str = 'default'
    password: str
    celery_db_index: int
    store_db_index: int
    bot_db_index: int
    api_db_index: int
    encoding: str = 'utf8'
    decode_responses: bool = False

    def get_redis_attributes(self, index: int) -> dict[str, str | int | bool]:
        return {
            'url': self.get_connection_url(index),
            'encoding': self.encoding,
            'decode_responses': self.decode_responses,
        }

    def get_connection_url(self, index: int) -> str:
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}//{index}'


REDIS_CONFIG = RedisConfig()
