from fastapi import Response

from backend.api.auth.scheme import TokenPayload
from backend.api.auth.security import JWT
from backend.config.backend import BACKEND_CONFIG


async def set_refresh(payload: TokenPayload, response: Response = Response) -> str:
    refresh_token = JWT.encode(payload.model_dump())
    response.set_cookie(BACKEND_CONFIG.refresh, refresh_token, BACKEND_CONFIG.refresh_token_ttl)
    return refresh_token
