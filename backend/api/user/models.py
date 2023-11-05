from uuid import uuid4

from sqlalchemy import func, UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.api.base_classes.models import Base
from backend.api.user.mixin import UserMixin


class User(UserMixin, Base):
    __tablename__ = 'UserTable'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, server_default=func.gen_random_uuid()
    )

    name: Mapped[str] = mapped_column(String(32), nullable=True)
    surname: Mapped[str] = mapped_column(String(32), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(32), nullable=True)

    login: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
