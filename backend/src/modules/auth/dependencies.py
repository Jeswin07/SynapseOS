import uuid

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.repository import UserRepository
from src.modules.auth.token_service import (
    decode_token,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(
        oauth2_scheme,
    ),
    db: Session = Depends(
        get_db,
    ),
):
    """
    Retrieve the currently authenticated user.

    Args:
        token: JWT access token.
        db: Database session.

    Returns:
        Authenticated User.

    Raises:
        HTTPException:
            If authentication fails.
    """

    try:

        payload = decode_token(token)

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )

    repository = UserRepository(db)

    user = repository.get_by_id(
        uuid.UUID(payload["sub"]),
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user