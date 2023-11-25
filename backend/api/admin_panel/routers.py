import random
import plotly.express as px
from datetime import datetime, timedelta

import pandas as pd
from fastapi import APIRouter, status, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from starlette.requests import Request

from backend.api.auth.security import Hasher
from backend.api.collection.models import Collection, CollectionDownloadQueryHistory
from backend.api.collection.tasks import predict_requests_in_hour
from backend.api.user.models import User
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


@admin_panel_router.post(
    path='/create-collections/monday-spam/',
    status_code=status.HTTP_201_CREATED
)
async def create_collections(session: AsyncSession = Depends(get_session_generator)):
    users: list[User] = (await User.get_all(session)).all()
    to_insert = []
    for hour in range(24):
        author_id = random.choice(users).id
        to_insert.append({'author_id': author_id, 'name': f'the most frequent caller at {hour} hour'})

    collections = (await session.scalars(
        insert(Collection).returning(Collection, sort_by_parameter_order=True), to_insert
    )).all()

    to_insert = []
    for hour, collection in enumerate(collections):
        user = random.choice(users)
        collection = random.choice(collections)
        # file_size = random.randint(1, 1 * 1024 * 1024 * 1024)
        file_size = 1

        now = datetime.now() + timedelta(days=6)
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
        hour: int,
        session: AsyncSession = Depends(get_session_generator)
):
    df = pd.DataFrame(
        [
            {'collection_id': item.collection_id, 'file_size': item.file_size, 'hour': item.created_at.hour}
            for item in await CollectionDownloadQueryHistory.get_history(session)
        ]
    )
    predict_collection, results_df = predict_requests_in_hour(df, hour)

    print(predict_collection)
    fig = px.scatter(x=results_df['distance'], y=results_df['predictions'], log_x=True, log_y=True)
    fig.write_html("/src/frontend/result.html")
    context = {"request": request}
    return templates.TemplateResponse("result.html", context)


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
