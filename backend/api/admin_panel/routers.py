import random
from typing import Literal

from datetime import datetime, timedelta

import pandas as pd
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from starlette.requests import Request

from backend.api.auth.security import Hasher
from backend.api.base_classes.models import engine, Base
from backend.api.collection.models import Collection, CollectionDownloadQueryHistory
from backend.api.collection.tasks import calculate_parameters_weights, prepare_calls_history_df, save_fig_to_html
from backend.api.photo.models import Photo
from backend.api.user.models import User
from backend.cache.redis_ import RedisContextManager
from backend.config.backend import LOGIC_CONFIG
from backend.depends.session import get_session_generator
from backend.main import templates

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


@admin_panel_router.get(
    path='/get-redis-keys/'
)
async def get_redis_keys():
    async with RedisContextManager() as redis:
        return await redis.get_keys()


@admin_panel_router.post(
    path='/create-collections/monday-spam/',
    status_code=status.HTTP_201_CREATED
)
async def create_collections(session: AsyncSession = Depends(get_session_generator)):
    users: list[User] = (await User.get_all(session)).all()
    to_insert = []
    for hour in range(24):
        author_id = random.choice(users).id
        to_insert.append({'author_id': author_id, 'name': f'collection {hour}'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for hour, collection in enumerate(collections):
        user = random.choice(users)
        file_size = (hour + 1) * 100000

        now = datetime.now() - timedelta(days=6)
        created_at = datetime(
            year=now.year, month=now.month, day=now.day, hour=hour, minute=now.minute, second=now.second
        )
        to_insert.append(
            {'collection_id': collection.id, 'sender_id': user.id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)


@admin_panel_router.get(
    path='/check-predication-by-hour/',
    status_code=status.HTTP_200_OK
)
async def check_predication_by_hour(
        request: Request,
        hour: int = Query(ge=0, le=23),
        session: AsyncSession = Depends(get_session_generator)
):
    df = pd.DataFrame(
        [
            {
                'name': item.collection.name,
                'collection_id': item.collection_id,
                'file_size': item.file_size,
                'sender_id': item.sender_id,
                'hour': item.created_at.hour,
            }
            for item in await CollectionDownloadQueryHistory.get_history(session)
        ]
    )
    df = prepare_calls_history_df(df, hour)
    df, normalized_weights = calculate_parameters_weights(df)
    save_fig_to_html(df)
    return normalized_weights


@admin_panel_router.get(
    path='/dashboard/',
    status_code=status.HTTP_200_OK
)
async def get_dashboard_hour(
        request: Request,
        index: Literal['0', '1', '2', '3', '4'] = None,
        parameter: Literal['name', 'file_size', 'senders_count', 'hour_repeats', 'proximity_to_target_hour'] = None,
):
    if index is not None:
        parameter = ['name', 'file_size', 'senders_count', 'hour_repeats', 'proximity_to_target_hour'][int(index)]
    context = {"request": request}
    return templates.TemplateResponse(f"{parameter}.html", context)


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
    for _ in range(1_000):
        user = random.choice(users)
        collection = random.choice(collections)
        file_size = random.randint(1, 1 * 1024 * 1024 * 1024)
        created_at = FAKE.date_time()
        to_insert.append(
            {'collection_id': collection.id, 'sender_id': user.id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)


@admin_panel_router.post(
    path='/create-data-to-check-proximity-to-target-hour-param/',
    status_code=status.HTTP_201_CREATED
)
async def create_data_to_check_proximity_to_target_hour_param(
        session: AsyncSession = Depends(get_session_generator),
):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    login = FAKE.profile(fields=["username"])["username"]
    password = Hasher.get_password_hash(login)
    name = FAKE.first_name()
    surname = FAKE.last_name()
    patronymic = FAKE.middle_name()
    user = await session.scalar(
        insert(User).returning(User, sort_by_parameter_order=True),
        {'login': login, 'password': password, 'name': name, 'surname': surname, 'patronymic': patronymic}
    )

    author_id = user.id
    to_insert = []
    for hour in range(24):
        to_insert.append({'author_id': author_id, 'name': f'collection {hour}'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for collection in collections:
        to_insert.append(
            {
                'collection_id': collection.id,
                'author_id': collection.author_id,
                'name': f'{collection.name} photo',
                'file': LOGIC_CONFIG.image
            }
        )
    await session.execute(insert(Photo), to_insert)

    file_size = 1 * 1024 * 1024
    to_insert = []
    for hour, collection in enumerate(collections):
        now = datetime.utcnow()
        created_at = datetime(
            year=now.year, month=now.month, day=now.day, hour=hour, minute=now.minute, second=now.second
        )
        to_insert.append(
            {'collection_id': collection.id, 'sender_id': user.id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)


@admin_panel_router.post(
    path='/create-data-to-check-file-size-param/',
    status_code=status.HTTP_201_CREATED
)
async def create_data_to_check_file_size_param(
        session: AsyncSession = Depends(get_session_generator),
):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    login = FAKE.profile(fields=["username"])["username"]
    password = Hasher.get_password_hash(login)
    name = FAKE.first_name()
    surname = FAKE.last_name()
    patronymic = FAKE.middle_name()
    user = await session.scalar(
        insert(User).returning(User, sort_by_parameter_order=True),
        {'login': login, 'password': password, 'name': name, 'surname': surname, 'patronymic': patronymic}
    )

    author_id = user.id
    to_insert = []
    for hour in range(24):
        to_insert.append({'author_id': author_id, 'name': f'collection {hour}'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for collection in collections:
        to_insert.append(
            {
                'collection_id': collection.id,
                'author_id': collection.author_id,
                'name': f'{collection.name} photo',
                'file': LOGIC_CONFIG.image
            }
        )
    await session.execute(insert(Photo), to_insert)

    to_insert = []
    for hour, collection in enumerate(collections):
        file_size = (hour + 1) * 1024 * 1024
        created_at = datetime.utcnow()
        to_insert.append(
            {'collection_id': collection.id, 'sender_id': user.id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)


@admin_panel_router.post(
    path='/create-data-to-check-senders-count-param/',
    status_code=status.HTTP_201_CREATED
)
async def create_data_to_check_senders_count_param(
        session: AsyncSession = Depends(get_session_generator),
):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    to_insert = []
    for _ in range(10):
        login = FAKE.profile(fields=["username"])["username"]
        password = Hasher.get_password_hash(login)
        name = FAKE.first_name()
        surname = FAKE.last_name()
        patronymic = FAKE.middle_name()
        to_insert.append(
            {'login': login, 'password': password, 'name': name, 'surname': surname, 'patronymic': patronymic}
        )
    users = (await session.scalars(insert(User).returning(User, sort_by_parameter_order=True), to_insert)).all()

    to_insert = []
    for hour, user in enumerate(users):
        author_id = random.choice(users).id
        to_insert.append({'author_id': author_id, 'name': f'collection {hour}'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for collection in collections:
        to_insert.append(
            {
                'collection_id': collection.id,
                'author_id': collection.author_id,
                'name': f'{collection.name} photo',
                'file': LOGIC_CONFIG.image
            }
        )
    await session.execute(insert(Photo), to_insert)

    file_size = 1 * 1024 * 1024
    to_insert = []
    for _ in range(50):
        collection_id = random.choice(collections).id
        sender_id = random.choice(users).id
        created_at = datetime.utcnow()
        to_insert.append(
            {'collection_id': collection_id, 'sender_id': sender_id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)


@admin_panel_router.post(
    path='/create-data-to-check-hour-repeats-param/',
    status_code=status.HTTP_201_CREATED
)
async def create_data_to_check_hour_repeats_param(
        session: AsyncSession = Depends(get_session_generator),
):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    login = FAKE.profile(fields=["username"])["username"]
    password = Hasher.get_password_hash(login)
    name = FAKE.first_name()
    surname = FAKE.last_name()
    patronymic = FAKE.middle_name()
    user = await session.scalar(
        insert(User).returning(User, sort_by_parameter_order=True),
        {'login': login, 'password': password, 'name': name, 'surname': surname, 'patronymic': patronymic}
    )

    to_insert = []
    for id_ in range(10):
        author_id = user.id
        to_insert.append({'author_id': author_id, 'name': f'collection {id_}'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for collection in collections:
        to_insert.append(
            {
                'collection_id': collection.id,
                'author_id': collection.author_id,
                'name': f'{collection.name} photo',
                'file': LOGIC_CONFIG.image
            }
        )
    await session.execute(insert(Photo), to_insert)

    file_size = 1 * 1024 * 1024
    to_insert = []
    for _ in range(100):
        collection_id = random.choice(collections).id
        sender_id = user.id
        now = datetime.utcnow()
        hour = random.randint(0, 23)
        created_at = datetime(
            year=now.year, month=now.month, day=now.day, hour=hour, minute=now.minute, second=now.second
        )
        to_insert.append(
            {'collection_id': collection_id, 'sender_id': sender_id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)


@admin_panel_router.post(
    path='/create-data-shuffle/',
    status_code=status.HTTP_201_CREATED
)
async def create_data_to_check_hour_repeats_param(
        session: AsyncSession = Depends(get_session_generator),
):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    to_insert = []
    for _ in range(random.randint(20, 50)):
        login = FAKE.profile(fields=["username"])["username"]
        password = Hasher.get_password_hash(login)
        name = FAKE.first_name()
        surname = FAKE.last_name()
        patronymic = FAKE.middle_name()
        to_insert.append(
            {'login': login, 'password': password, 'name': name, 'surname': surname, 'patronymic': patronymic}
        )
    users = (await session.scalars(insert(User).returning(User, sort_by_parameter_order=True), to_insert)).all()

    to_insert = []
    for id_ in range(random.randint(50, 100)):
        author_id = random.choice(users).id
        to_insert.append({'author_id': author_id, 'name': f'collection {id_}'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for collection in collections:
        to_insert.append(
            {
                'collection_id': collection.id,
                'author_id': collection.author_id,
                'name': f'{collection.name} photo',
                'file': LOGIC_CONFIG.image
            }
        )
    await session.execute(insert(Photo), to_insert)

    to_insert = []
    for _ in range(100):
        collection_id = random.choice(collections).id
        sender_id = random.choice(users).id
        now = datetime.utcnow()
        hour = random.randint(0, 23)
        file_size = random.randint(1, 50) * 1024 * 1024
        created_at = datetime(
            year=now.year, month=now.month, day=now.day, hour=hour, minute=now.minute, second=now.second
        )
        to_insert.append(
            {'collection_id': collection_id, 'sender_id': sender_id, 'file_size': file_size, 'created_at': created_at}
        )
    await session.execute(insert(CollectionDownloadQueryHistory), to_insert)
