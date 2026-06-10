from datetime import UTC, datetime, timedelta

import jwt

from src.core.config import settings


def create_access_token(
    user_id: str,
    tenant_id: str,
    role: str,
) -> str:

    expire = (
        datetime.now(UTC)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(
    token: str,
) -> dict:

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[
            settings.jwt_algorithm
        ],
    )

def create_refresh_token(
    user_id: str,
) -> str:

    expire = (
        datetime.now(UTC)
        + timedelta(
            days=settings.refresh_token_expire_days
        )
    )

    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def is_access_token(
    payload: dict,
) -> bool:

    return (
        payload.get("type")
        == "access"
    )

def is_refresh_token(
    payload: dict,
) -> bool:

    return (
        payload.get("type")
        == "refresh"
    )