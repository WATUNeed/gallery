import typing

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession


class UserMixin:
    @classmethod
    async def get_by_login(cls, session: AsyncSession, login: str) -> typing.Self:
        query = sa.select(
            cls
        ).where(
            cls.login == login
        )
        result = (await session.execute(query)).one_or_none()
        return None if result is None else result[0]

    @classmethod
    async def get_all(cls, session: AsyncSession) -> sa.ScalarResult[typing.Self]:
        return await session.scalars(sa.select(cls))
