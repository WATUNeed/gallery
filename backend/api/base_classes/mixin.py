from typing import Self

from sqlalchemy import Update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseMixin:
    async def create(self, session: AsyncSession) -> Self:
        session.add(self)
        await session.flush()
        return self

    async def update(self, session: AsyncSession, data_to_update: Self) -> Self:
        updated_instance = await session.execute(Update(self), data_to_update)
        return updated_instance
