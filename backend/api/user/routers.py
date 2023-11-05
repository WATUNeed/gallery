from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.user.models import User
from backend.api.user.scheme import ShareUserScheme, UpdateUser
from backend.depends.session import get_session_generator

users_router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@users_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=list[ShareUserScheme],
)
async def get_users(
        session: AsyncSession = Depends(get_session_generator),
) -> list[ShareUserScheme]:
    users = await User.get_all(session)
    return users


@users_router.put(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=ShareUserScheme,
)
async def update_users(
        user_id: UUID,
        body: UpdateUser = Body(...),
        session: AsyncSession = Depends(get_session_generator),
) -> ShareUserScheme:
    user = await User.update(session, user_id, body.model_dump())
    return ShareUserScheme.model_validate(user)