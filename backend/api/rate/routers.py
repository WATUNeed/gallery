from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api.auth.scheme import TokenPayload
from backend.api.photo.models import Photo
from backend.depends.access_validation import CheckToken
from backend.depends.session import get_session_generator

rating_router = APIRouter(
    prefix='collections/photos/rate',
    tags=['Photos']
)


# @rating_router.post(
#     path='/',
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_rate(
#         body: RatePOST = Body(...),
#         user: TokenPayload = Depends(CheckToken()),
#         session: AsyncSession = Depends(get_session_generator),
# ) -> Photo.View:
#     pass
