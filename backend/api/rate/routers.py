from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api.auth.scheme import TokenPayload
from backend.api.photo.models import Photo
from backend.api.rate.models import Rate
from backend.api.rate.scheme import RateScheme
from backend.depends.access_validation import get_current_user
from backend.depends.session import get_session_generator

rating_router = APIRouter(
    prefix='/collections/photos/rate',
    tags=['Photos']
)


@rating_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
)
async def create_rate(
        body: RateScheme.PostBody = Body(...),
        user: TokenPayload = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_generator),
):
    rate = Rate(
        author_id=user.sub,
        rate=body.rate,
    )
    photo = await session.get(Photo, body.photo_id)
    rate.photos.append(photo)
    await rate.create(session)
