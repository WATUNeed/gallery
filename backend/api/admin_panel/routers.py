import random

from fastapi import APIRouter, status, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from backend.api.auth.security import Hasher
from backend.api.collection.models import Collection, CollectionDownloadQueryHistory
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
    for _ in range(1_000):
        login = f'{FAKE.profile(fields=["username"])["username"]}_{random.randint(0, 999999999999)}'
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


@admin_panel_router.post(
    path='/create-collections/',
    status_code=status.HTTP_201_CREATED
)
async def create_collections(
        session: AsyncSession = Depends(get_session_generator),
):
    users: list[User] = (await User.get_all(session)).all()
    to_insert = []
    for _ in range(1_000):
        author_id = random.choice(users).id
        name = FAKE.profile(fields=["username"])["username"]
        to_insert.append({'author_id': author_id, 'name': name})
    await session.execute(insert(Collection), to_insert)

@admin_panel_router.post(
    path='/create-download-collections-query-history/',
    status_code=status.HTTP_201_CREATED
)
async def create_download_collections_query_history(
        session: AsyncSession = Depends(get_session_generator),
):
    users: list[User] = (await User.get_all(session)).all()
    collections: list[Collection] = (await Collection.get_with_related(session)).all()
    to_insert = []
    for _ in range(100_000):
        user = random.choice(users)
        collection = random.choice(collections)
        file_size = random.randint(1, 1 * 1024 * 1024 * 1024)
        created_at = FAKE.date_time()
        to_insert.append(
            {'collection_id': collection.id, 'sender_id': user.id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)
