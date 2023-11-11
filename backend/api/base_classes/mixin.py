import typing
from typing import Self, Any
from uuid import UUID

from sqlalchemy import Update
from sqlalchemy.ext.asyncio import AsyncSession

class BaseMixin:
    @classmethod
    async def update(cls, session: AsyncSession, id_: UUID | int, data_to_update: dict[str, Any]):
        query = Update(
            cls
        ).where(
            cls.id == id_
        )
        await session.execute(query, data_to_update)

    @classmethod
    async def delete(cls, session: AsyncSession, id_: UUID):
        instance = await session.get(cls, id_)
        await session.delete(instance)

    async def create(self, session: AsyncSession) -> Self:
        session.add(self)
        await session.flush()
        return self
