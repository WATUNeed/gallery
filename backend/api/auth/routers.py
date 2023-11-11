from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api.auth.exceptions import AuthException
from backend.api.auth.scheme import SignBody, TokenPayload, Token
from backend.api.auth.security import Hasher
from backend.api.user.exceptions import UserException
from backend.api.user.models import User
from backend.config.backend import BACKEND_CONFIG
from backend.depends.access_validation import CheckToken
from backend.depends.cookie_worker import set_refresh
from backend.depends.session import get_session_generator

auth_router = APIRouter(
    prefix='/auth',
    tags=['Authorization']
)


@auth_router.post(
    path='/sign-up/',
    status_code=status.HTTP_201_CREATED,
    response_model=Token
)
async def sign_up(
        body: SignBody = Body(...),
        session: AsyncSession = Depends(get_session_generator),
        response: Response = Response(),
) -> Token:
    if await User.get_by_login(session, body.login) is not None:
        raise UserException.LoginAlreadyUsed

    body.password = Hasher.get_password_hash(body.password)

    user = await User(
        login=body.login,
        password=body.password,
    ).create(session)

    refresh_token_payload = TokenPayload(
        sub=str(user.id),
        exp=datetime.utcnow() + timedelta(seconds=BACKEND_CONFIG.refresh_token_ttl)
    )
    cookie_token = await set_refresh(refresh_token_payload, response)
    return Token(token=cookie_token)


@auth_router.post(
    path='/sign-in/',
    status_code=status.HTTP_201_CREATED,
    response_model=Token
)
async def sign_in(
        body: SignBody = Body(...),
        session: AsyncSession = Depends(get_session_generator),
        response: Response = Response(),
) -> Token:
    user = await User.get_by_login(session, body.login)
    if user is None:
        raise UserException.NotFound
    if not Hasher.verify_password(body.password, user.password):
        raise AuthException.TokenNotFound

    refresh_token_payload = TokenPayload(
        sub=str(user.id),
        exp=datetime.utcnow() + timedelta(seconds=BACKEND_CONFIG.refresh_token_ttl)
    )
    cookie_token = await set_refresh(refresh_token_payload, response)
    return Token(token=cookie_token)


@auth_router.delete(
    path='/logout/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
        user_data: TokenPayload = Depends(CheckToken()),
        response: Response = Response,
):
    response.delete_cookie(BACKEND_CONFIG.refresh)
