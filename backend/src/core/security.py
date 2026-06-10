from fastapi import (
    Depends,
    HTTPException,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.repository import (
    UserRepository,
)
from src.modules.auth.token_service import (
    decode_token,
)

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):

    try:
        payload = decode_token(credentials.credentials)

        user_id = payload["sub"]

        repository = UserRepository(db)

        user = repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
