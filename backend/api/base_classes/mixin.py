from typing import Self, Any
from uuid import UUID

from sqlalchemy import Update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseMixin:
    @classmethod
    async def update(cls, session: AsyncSession, id_: UUID | int, data_to_update: dict[str, Any]) -> Self:
        await session.execute(Update(cls).where(cls.id == id_), data_to_update)
        return await session.get_one(cls, id_)

    async def create(self, session: AsyncSession) -> Self:
        session.add(self)
        await session.flush()
        return self
