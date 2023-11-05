from pydantic_settings import BaseSettings


class TimeConfig(BaseSettings):
    date_format: str = '%d-%m-%Y'
    time_format: str = '%H:%M:%S'
    full_format: str = '%d-%m-%YT%H:%M:%S'


TIME_CONFIG = TimeConfig()
