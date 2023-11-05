from pydantic import BaseModel
from starlette import status


class BaseScheme(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

    class DictConfig:
        orm_mode = True
        from_attributes = True
        populate_by_name = True
        use_enum_values = True
        arbitrary_types_allowed = True


class BaseExceptionResponse(BaseModel):
    description: str

    class DictConfig:
        from_attributes = True
        populate_by_name = True
        use_enum_values = True
        arbitrary_types_allowed = True


class NotFoundResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_404_NOT_FOUND


class ConflictResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_409_CONFLICT


class BadRequestResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_400_BAD_REQUEST


class ForbiddenResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_403_FORBIDDEN


class UnauthorizedResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_401_UNAUTHORIZED


class ValidationErrorResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY


class GoneResponse(BaseExceptionResponse):
    status_code: int = status.HTTP_410_GONE
