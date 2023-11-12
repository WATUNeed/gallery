import os
import shutil
from datetime import datetime
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, status, Body, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from backend.api.auth.scheme import TokenPayload
from backend.api.collection.models import Collection, CollectionDownloadQueryHistory
from backend.api.collection.scheme import CollectionScheme
from backend.config.backend import BACKEND_CONFIG
from backend.depends.access_validation import get_current_user
from backend.depends.session import get_session_generator

collection_router = APIRouter(
    prefix='/collections',
    tags=['Collections']
)


@collection_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=CollectionScheme.View,
)
async def create_collection(
        body: CollectionScheme.PostBody = Body(...),
        user: TokenPayload = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_generator),
) -> CollectionScheme.View:
    collection = await Collection(
        author_id=user.sub,
        name=body.name,
        description=body.description
    ).create(session)
    return collection


@collection_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=list[CollectionScheme.WithRelated],
)
async def get_collections(
        user: TokenPayload = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_generator),
) -> list[CollectionScheme.WithRelated]:
    collections = await Collection.get_with_related(session)
    return collections


@collection_router.put(
    path='/',
    status_code=status.HTTP_200_OK
)
async def update_collection(
        body: CollectionScheme.PutBody = Body(...),
        user: TokenPayload = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_generator),
):
    await Collection.update(session, body.id, body.model_dump())


@collection_router.delete(
    path='/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_collection(
        collection_id: UUID,
        user: TokenPayload = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_generator),
):
    await Collection.delete(session, collection_id)


@collection_router.get(
    path='/download/',
    status_code=status.HTTP_200_OK
)
async def download_collection(
        background_tasks: BackgroundTasks,
        collection_id: UUID,
        user: TokenPayload = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_generator),
):
    collection = await session.get(Collection, collection_id)
    images = await Collection.get_image(session, collection_id)

    if not Path(BACKEND_CONFIG.collection_path).is_dir():
        os.mkdir(BACKEND_CONFIG.collection_path)
    if not Path(f'{BACKEND_CONFIG.collection_path}{collection_id}').is_dir():
        os.mkdir(f'{BACKEND_CONFIG.collection_path}{collection_id}')
        os.mkdir(f'{BACKEND_CONFIG.collection_path}{collection_id}/images/')
    else:
        shutil.rmtree(f'{BACKEND_CONFIG.collection_path}{collection_id}/images/')
        os.mkdir(f'{BACKEND_CONFIG.collection_path}{collection_id}/images/')

    for image in images:
        with open(f'{BACKEND_CONFIG.collection_path}{collection_id}/images/{image.name}.png', mode='wb') as file:
            file.write(image.file)

    shutil.make_archive(
        f'{BACKEND_CONFIG.collection_path}{collection_id}/{collection.name}',
        'zip',
        f'{BACKEND_CONFIG.collection_path}{collection_id}/images'
    )
    response = FileResponse(
        path=f'{BACKEND_CONFIG.collection_path}{collection_id}/{collection.name}.zip',
        filename=f"{collection.name}.zip",
    )
    file_size = os.path.getsize(f'{BACKEND_CONFIG.collection_path}{collection_id}/{collection.name}.zip')
    background_tasks.add_task(save_request, session, collection_id, user.sub, file_size)
    background_tasks.add_task(delete_collection_zip_files_task, collection_id)
    return response


async def delete_collection_zip_files_task(collection_id: UUID):
    shutil.rmtree(f'{BACKEND_CONFIG.collection_path}{collection_id}/')


async def save_request(
        session: AsyncSession,
        collection_id: UUID,
        sender_id: UUID,
        file_size: int
):
    await CollectionDownloadQueryHistory(
        collection_id=collection_id,
        sender_id=sender_id,
        file_size=file_size
    ).create(session)
