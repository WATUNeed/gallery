from fastapi import HTTPException, status


class AuthException:
    TokenNotFound = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token not found in cookies or bearer.'
    )
    InvalidCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials.'
    )
