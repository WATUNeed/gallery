from string import ascii_lowercase
from typing import Any

from starlette.responses import JSONResponse

from backend.api.base_classes.scheme import BaseExceptionResponse


class BaseHTTPException(Exception):
    __slots__ = ('response',)

    response: BaseExceptionResponse

    @classmethod
    def get_response(cls) -> JSONResponse:
        return JSONResponse(status_code=cls.response.status_code, content=cls.response.model_dump())

    @property
    def map(self) -> dict[int | str, dict[str, str | dict[str, dict[str | Any]]]]:
        description = ''.join(
            char if char in ascii_lowercase else f' {char}' for char in self.response.__class__.__name__
        )
        return {
            self.response.status_code: {
                "description": description,
                "content": {
                    "application/json": {
                        "example": self.response.model_dump()
                    }
                }
            }
        }