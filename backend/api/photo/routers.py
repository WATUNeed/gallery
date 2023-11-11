from uuid import UUID

from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.scheme import RefreshToken
from backend.api.photo.models import Photo
from backend.api.photo.scheme import CreatePhoto, GetPhotoWithRelated, GetPhoto
from backend.depends.access_validation import CheckToken
from backend.depends.session import get_session_generator

photo_router = APIRouter(
    prefix='/collections/photos',
    tags=['Photos']
)


@photo_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=GetPhoto,
)
async def create_photo(
        body: CreatePhoto = Body(...),
        user: RefreshToken = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
) -> GetPhoto:
    photo = await Photo(**body.model_dump(), author_id=user.sub).create(session)
    return photo


@photo_router.delete(
    path='/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_photo(
        photo_id: UUID,
        user: RefreshToken = Depends(CheckToken()),
        session: AsyncSession = Depends(get_session_generator),
):
    await Photo.delete(session, photo_id)
