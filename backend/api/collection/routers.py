from uuid import UUID

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.scheme import TokenPayload
from backend.api.collection.models import Collection
from backend.api.collection.scheme import CollectionScheme
from backend.depends.access_validation import CheckToken
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
        user: TokenPayload = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
) -> CollectionScheme.View:
    collection = await Collection(
        author_id=user.sub,
        name=body.name,
        description=body.description
    ).create(session)
    return CollectionScheme.View.model_validate(collection)


@collection_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=list[CollectionScheme.WithRelated],
)
async def get_collections(
        user: TokenPayload = Depends(CheckToken()),
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
        user: TokenPayload = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
):
    await Collection.update(session, body.id, body.model_dump())


@collection_router.delete(
    path='/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_collection(
        collection_id: UUID,
        user: TokenPayload = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
):
    await Collection.delete(session, collection_id)
