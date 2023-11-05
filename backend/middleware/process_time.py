from time import perf_counter

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class ProcessTimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = perf_counter()
        response = await call_next(request)
        process_time = perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
