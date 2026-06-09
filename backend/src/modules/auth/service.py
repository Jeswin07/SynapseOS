import uuid

from sqlalchemy.orm import Session

from src.models.user import User
from src.models.enums import UserRole

from src.modules.auth.repository import UserRepository
from src.modules.auth.security import (
    hash_password,
    verify_password,
)
from src.modules.auth.token_service import (
    create_access_token,
)


class AuthService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = UserRepository(db)

    def register(
        self,
        email: str,
        full_name: str,
        password: str,
        tenant_id: str,
    ):

        existing_user = (
            self.repository.get_by_email(email)
        )

        if existing_user:
            raise ValueError(
                "User already exists"
            )

        user = User(
            tenant_id=uuid.UUID(tenant_id),
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=UserRole.ADMIN,
        )

        return self.repository.create(user)

    def login(
        self,
        email: str,
        password: str,
    ):

        user = (
            self.repository.get_by_email(email)
        )

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid credentials"
            )

        return create_access_token(
            str(user.id),
            str(user.tenant_id),
            user.role.value,
        )