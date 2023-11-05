from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from backend.api.base_classes.mixin import BaseMixin
from backend.config.database import DB_CONFIG


class Base(BaseMixin, AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __repr__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in self.to_dict().items())
        return f'{self.__class__.__name__}({attrs})'

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}

    @classmethod
    def get_scheme(cls) -> list[str]:
        return [field.name for field in cls.__table__.c]


meta = MetaData()

engine = create_async_engine(
    DB_CONFIG.connection_url,
    poolclass=NullPool,
    echo=DB_CONFIG.ddl_show,
)
Session = async_sessionmaker(engine, expire_on_commit=False)
