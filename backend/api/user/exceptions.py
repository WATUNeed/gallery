from backend.api.base_classes.exceptions import BaseHTTPException
from backend.api.base_classes.scheme import BadRequestResponse, NotFoundResponse


class EmailAlreadyInUseException(BaseHTTPException):
    response = BadRequestResponse(description='EMAIL_ALREADY_IN_USE')


class LoginAlreadyInUseException(BaseHTTPException):
    response = BadRequestResponse(description='This login already in used.')


class TelegramAlreadyInUseException(BaseHTTPException):
    response = BadRequestResponse(description='TELEGRAM_ALREADY_IN_USE')


class UserNotFoundException(BaseHTTPException):
    response = NotFoundResponse(description="User not found.")


class PermissionDenyUpdateException(BaseHTTPException):
    response = BadRequestResponse(description='CANNOT_CHANGE_DATA_ABOUT_OTHER_USERS')
