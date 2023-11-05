from uuid import UUID

from fastapi import Request, Response

from backend.api.auth.exceptions import RefreshTokenNotFoundException
from backend.api.auth.scheme import RefreshToken
from backend.api.auth.security import JWT
from backend.config.backend import BACKEND_CONFIG


async def get_data_with_update_refresh(request: Request = Request, response: Response = Response) -> RefreshToken:
    token = request.cookies.get(BACKEND_CONFIG.refresh)
    if token is None:
        raise RefreshTokenNotFoundException
    payload = RefreshToken.model_validate(JWT.decode(token))
    token = JWT.encode(payload.model_dump())
    response.set_cookie(BACKEND_CONFIG.refresh, token, BACKEND_CONFIG.refresh_token_ttl)
    payload.user_id = UUID(payload.user_id)
    return payload


async def set_refresh(payload: RefreshToken, response: Response = Response) -> str:
    refresh_token = JWT.encode(payload.model_dump())
    response.set_cookie(BACKEND_CONFIG.refresh, refresh_token, BACKEND_CONFIG.refresh_token_ttl)
    return refresh_token
