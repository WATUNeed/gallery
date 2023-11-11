from uuid import UUID

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.scheme import RefreshToken
from backend.api.collection.models import Collection
from backend.api.collection.scheme import CreateCollection, GetCollection, GetCollectionWithRelated, UpdateCollection
from backend.depends.access_validation import CheckToken
from backend.depends.session import get_session_generator

collection_router = APIRouter(
    prefix='/collections',
    tags=['Collections']
)


@collection_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=GetCollection,
)
async def create_collection(
        body: CreateCollection = Body(...),
        user: RefreshToken = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
) -> GetCollection:
    collection = await Collection(
        author_id=user.sub,
        name=body.name,
        description=body.description
    ).create(session)
    return GetCollection.model_validate(collection)


@collection_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=list[GetCollectionWithRelated],
)
async def get_collections(
        user: RefreshToken = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
) -> list[GetCollectionWithRelated]:
    collections = await Collection.get_with_related(session)
    return collections


@collection_router.put(
    path='/',
    status_code=status.HTTP_200_OK
)
async def update_collections(
        body: UpdateCollection = Body(...),
        user: RefreshToken = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
):
    await Collection.update(session, body.id, body.model_dump())


@collection_router.delete(
    path='/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_collections(
        collection_id: UUID,
        user: RefreshToken = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
):
    await Collection.delete(session, collection_id)
