from jose import jwt, JWTError
import hashlib

from backend.api.auth.exceptions import AuthException
from backend.config.auth import AUTH_CONFIG


class Hasher:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return hashed_password == hashlib.sha256(plain_password.encode()).hexdigest()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()


class JWT:
    @staticmethod
    def encode(claims: dict) -> str:
        return jwt.encode(claims, AUTH_CONFIG.secret, AUTH_CONFIG.algorithm)

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(token, AUTH_CONFIG.secret, AUTH_CONFIG.algorithm)
        except JWTError:
            raise AuthException.InvalidCredentials
