from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

from models.user_model import UserInDB
from utils.settings import get_settings


class JWTException(Exception):
    pass


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as exc:
        raise JWTException("Token validation failed") from exc


def create_user_token(user: UserInDB) -> str:
    return create_access_token({"sub": str(user.id), "email": user.email})
