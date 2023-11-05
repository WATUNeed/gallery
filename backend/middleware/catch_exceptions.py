from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.api.base_classes.exceptions import BaseHTTPException


class RequestHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except BaseHTTPException as exc:
            return Response(status_code=exc.response.status_code, headers={'details': exc.response.description})
