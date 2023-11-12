from random import randint

from fastapi import APIRouter, status, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from backend.api.auth.security import Hasher
from backend.api.collection.models import Collection
from backend.api.user.models import User
from backend.depends.session import get_session_generator

admin_panel_router = APIRouter(
    prefix='/admin-panel',
    tags=['Admin Panel']
)

FAKE = Faker('ru_RU')


@admin_panel_router.post(
    path='/create-users/',
    status_code=status.HTTP_201_CREATED
)
async def create_users(
        session: AsyncSession = Depends(get_session_generator),
):
    to_insert = []
    for _ in range(10_000):
        login = f'{FAKE.profile(fields=["username"])["username"]}_{randint(0, 999999999999)}'
        if len(login) > 32:
            login = login[:31]
        password = Hasher.get_password_hash(login)
        name = FAKE.first_name()
        surname = FAKE.last_name()
        patronymic = FAKE.middle_name()
        to_insert.append(
            {'login': login, 'password': password, 'name': name, 'surname': surname, 'patronymic': patronymic}
        )
    await session.execute(insert(User), to_insert)

