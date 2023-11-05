from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserMixin:
    @classmethod
    async def get_by_login(cls, session: AsyncSession, login: str) -> Self:
        query = select(
            cls
        ).where(
            cls.login == login
        )
        result = (await session.execute(query)).one_or_none()
        return None if result is None else result[0]
