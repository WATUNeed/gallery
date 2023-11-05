import logging
from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='web_')

    title: str = 'Gallery'
    description: str = 'Gallery app'
    version: str = '1.0.1'
    debug: bool = True

    host: str
    port: int
    reload: bool = False
    logging_level: int = logging.DEBUG

    refresh: str = 'refresh'
    refresh_token_ttl: int = 2 * 60 * 100

    @cached_property
    def get_app_config(self) -> dict[str, str | bool | None]:
        return {
            "title": self.title,
            "version": self.version,
            "debug": self.debug,
            "description": self.description,
        }

    @cached_property
    def get_uvicorn_attr(self) -> dict[str, str | bool | None]:
        return {
            'host': self.host,
            'port': self.port,
            'reload': self.reload,
            'log_level': self.logging_level,
        }


class MiddlewareConfig(BaseSettings):
    origins: list[str] = [
        "http://localhost:3000"
    ]
    allow_methods: list[str] = [
        "GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"
    ]
    allow_headers: list[str] = [
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"
    ]
    allow_credentials: bool = True

    @cached_property
    def middleware_config(self) -> dict[str, str | bool | None]:
        return {
            'allow_origins': self.origins,
            'allow_methods': self.allow_methods,
            'allow_headers': self.allow_headers,
            'allow_credentials': self.allow_credentials,
        }


class LoggingConfig(BaseSettings):
    file_logging_level: int = logging.ERROR
    file_max_bytes: int = 10 * 1024 * 1024  # 10MB
    file_backup_count: int = 5
    file_logging_filename: str = "logs/error_log"
    logging_format: str = "%(levelname)s: [%(asctime)s] - %(message)s"
    logging_datefmt: str = "%Y-%m-%d %H:%M:%S"
    file_logging_mode: str = 'a+'

    @cached_property
    def get_file_logging_class_attributes(self) -> dict[str, str | int]:
        return {
            'filename': self.file_logging_filename,
            'maxBytes': self.file_max_bytes,
            'backupCount': self.file_backup_count,
            'mode': self.file_logging_mode
        }

    @cached_property
    def get_file_logging_formatter_attributes(self) -> dict[str, str]:
        return {
            'fmt': self.logging_format,
            'datefmt': self.logging_datefmt
        }


class LogicConfig(BaseSettings):
    edit_deadline_days: int = 1


BACKEND_CONFIG = BackendConfig()
MIDDLEWARE_CONFIG = MiddlewareConfig()
LOGGING_CONFIG = LoggingConfig()
LOGIC_CONFIG = LogicConfig()
