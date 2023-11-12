import os
import shutil
import tempfile
from pathlib import Path
from uuid import UUID
from zipfile import ZipFile

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from backend.api.auth.scheme import TokenPayload
from backend.api.collection.models import Collection
from backend.api.collection.scheme import CollectionScheme
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
        collection_id: UUID,
        session: AsyncSession = Depends(get_session_generator),
):
    collection = await session.get(Collection, collection_id)
    images = await Collection.get_image(session, collection_id)

    if not Path(f'/tmp/collections/').is_dir():
        os.mkdir('/tmp/collections/')
    if not Path(f'/tmp/collections/{collection_id}').is_dir():
        os.mkdir(f'/tmp/collections/{collection_id}')
        os.mkdir(f'/tmp/collections/{collection_id}/images/')
    else:
        shutil.rmtree(f'/tmp/collections/{collection_id}/images/')
        os.mkdir(f'/tmp/collections/{collection_id}/images/')

    for image in images:
        with open(f'/tmp/collections/{collection_id}/images/{image.name}.png', mode='wb') as file:
            file.write(image.file)

    shutil.make_archive(
        f'/tmp/collections/{collection_id}/{collection.name}',
        'zip',
        f'/tmp/collections/{collection_id}/images'
    )
    response = FileResponse(
        path=f'/tmp/collections/{collection_id}/{collection.name}.zip',
        filename=f"{collection.name}.zip"
    )
    return response
