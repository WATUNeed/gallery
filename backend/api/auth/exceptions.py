from backend.api.base_classes.exceptions import BaseHTTPException
from backend.api.base_classes.scheme import ForbiddenResponse, BadRequestResponse, NotFoundResponse, \
    UnauthorizedResponse, GoneResponse


class InvalidCredentialsException(BaseHTTPException):
    response = ForbiddenResponse(description='INVALID_CREDENTIALS')


class UserNeedToReactivateAccountException(BaseHTTPException):
    response = BadRequestResponse(description='USER_NEED_TO_REACTIVATE_ACCOUNT')


class TokenIsExpiresException(BaseHTTPException):
    response = ForbiddenResponse(description='TOKEN_IS_EXPIRES')


class TokenIsEmptyException(BaseHTTPException):
    response = BadRequestResponse(description='TOKEN_IS_EMPTY')


class TargetRoleIsEmptyException(BaseHTTPException):
    response = BadRequestResponse(description='TARGET_ROLE_IS_EMPTY')


class WrongRoleException(BaseHTTPException):
    response = ForbiddenResponse(description='USER_HAVE_WRONG_ROLE')


class RegistrationRequestException(BaseHTTPException):
    response = NotFoundResponse(description='REGISTER_REQUEST_FROM_TELEGRAM_NOT_FOUND')


class QRCodeRequestNotFoundException(BaseHTTPException):
    response = NotFoundResponse(description='QR_CODE_WAS_NOT_CREATED_OR_EXPIRED')


class RefreshTokenNotFoundException(BaseHTTPException):
    response = UnauthorizedResponse(description='REFRESH_TOKEN_NOT_FOUND_IN_COOKIE')


class InviteExpiresException(BaseHTTPException):
    response = BadRequestResponse(description='INVITE_EXPIRES')


class InvitationsOverException(BaseHTTPException):
    response = BadRequestResponse(description='THE_NUMBER_OF_USES_OF_THE_INVITATION_HAS_EXPIRED')


class TokenNotFoundException(BaseHTTPException):
    response = NotFoundResponse(description='TOKEN_NOT_FOUND_IN_STORAGE')


class TokenExpiresException(BaseHTTPException):
    response = GoneResponse(description='TOKEN_WAS_EXPIRED')
