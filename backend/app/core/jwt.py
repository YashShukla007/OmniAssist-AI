from datetime import datetime, timedelta, timezone

import jwt

from backend.app.config.settings import settings


def _configured_secret_key() -> str:
    if len(settings.SECRET_KEY) < 32:
        raise RuntimeError("SECRET_KEY must be configured with at least 32 characters before authentication can be used.")
    return settings.SECRET_KEY


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        _configured_secret_key(),
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str):
    return jwt.decode(
        token,
        _configured_secret_key(),
        algorithms=[settings.ALGORITHM],
    )
