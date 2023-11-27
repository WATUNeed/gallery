import typing
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.photo.models import Photo


class CollectionMixin:
    @classmethod
    async def get_with_related(cls, session: AsyncSession) -> sa.ScalarResult[typing.Self]:
        query = sa.select(
            cls
        ).options(
            selectinload(cls.author),
            selectinload(cls.photos)
        )
        return await session.scalars(query)

    @classmethod
    async def get_image(cls, session: AsyncSession, collection_id: UUID):
        query = sa.select(
            Photo.name,
            Photo.file
        ).join_from(
            cls, Photo, cls.photos
        ).where(
            cls.id == collection_id
        )
        return (await session.execute(query)).all()


class CollectionDownloadQueryHistoryMixin:
    @classmethod
    async def get_history(cls, session: AsyncSession):
        return await session.scalars(sa.select(cls).options(selectinload(cls.collection)))
