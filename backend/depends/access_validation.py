from uuid import UUID

from fastapi import Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.api.auth.exceptions import AuthException
from backend.api.auth.scheme import TokenPayload
from backend.api.auth.security import JWT
from backend.config.backend import BACKEND_CONFIG


class CheckToken(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(CheckToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request = Request, response: Response = Response) -> TokenPayload:
        token = request.cookies.get(BACKEND_CONFIG.refresh)
        if token is None:
            credentials: HTTPAuthorizationCredentials = await super(CheckToken, self).__call__(request)
            if credentials is None or credentials.scheme == 'Bearer':
                raise AuthException.TokenNotFound
            payload = TokenPayload.model_validate(JWT.decode(credentials.credentials))
        else:
            payload = TokenPayload.model_validate(JWT.decode(token))

        payload.sub = UUID(payload.sub)
        return payload


get_current_user = CheckToken()
