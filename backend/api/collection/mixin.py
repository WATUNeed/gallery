import typing

import sqlalchemy as sa
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CollectionMixin:
    @classmethod
    async def get_with_related(cls, session: AsyncSession) -> ScalarResult[typing.Self]:
        query = sa.select(
            cls
        ).options(
            selectinload(cls.author),
            selectinload(cls.photos)
        )
        return await session.scalars(query)
