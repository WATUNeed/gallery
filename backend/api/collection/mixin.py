import typing

import sqlalchemy as sa
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.base_classes.mixin import BaseMixin


if typing.TYPE_CHECKING:
    from backend.api.collection.models import Collection


def _collection():
    from backend.api.collection.models import Collection
    return Collection


class CollectionMixin(BaseMixin):
    @classmethod
    async def get_with_related(cls, session: AsyncSession) -> ScalarResult[typing.Self]:
        cls: _collection()
        query = sa.select(
            cls
        ).options(
            selectinload(cls.author),
            selectinload(cls.photos)
        )
        return await session.scalars(query)
