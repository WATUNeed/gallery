from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.base_classes.models import Session


async def get_session_generator() -> Generator[AsyncSession, None, None]:
    session = None
    try:
        session = Session()
        async with session.begin():
            yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.commit()
        await session.close()
