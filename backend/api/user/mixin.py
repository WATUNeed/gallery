from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.base_classes.mixin import BaseMixin
from backend.api.user.scheme import ShareUserScheme


class UserMixin(BaseMixin):
    @classmethod
    async def get_by_login(cls, session: AsyncSession, login: str) -> Self:
        query = select(
            cls
        ).where(
            cls.login == login
        )
        result = (await session.execute(query)).one_or_none()
        return None if result is None else result[0]

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[ShareUserScheme]:
        result = (await session.execute(select(cls))).scalars()
        return [ShareUserScheme.model_validate(user) for user in result]
