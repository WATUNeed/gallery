from uuid import UUID

from backend.api.base_classes.scheme import BaseScheme


class UserScheme:
    class PutBody(BaseScheme):
        name: str | None = None
        surname: str | None = None
        patronymic: str | None = None

    class ShareView(BaseScheme):
        id: UUID
        name: str | None = None
        surname: str | None = None
        patronymic: str | None = None
        login: str
