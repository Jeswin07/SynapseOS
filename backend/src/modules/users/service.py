from sqlalchemy.orm import Session

from src.models.user import User
from src.modules.auth.security import (
    hash_password,
)
from src.modules.users.repository import (
    UserManagementRepository,
)


class UserManagementService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = (
            UserManagementRepository(db)
        )

    def create_user(
        self,
        current_user,
        full_name: str,
        email: str,
        password: str,
        role,
    ):

        existing_user = (
            self.repository.get_by_email(email)
        )

        if existing_user:
            raise ValueError(
                "User already exists"
            )

        try:

            user = User(
                tenant_id=current_user.tenant_id,
                full_name=full_name,
                email=email,
                hashed_password=hash_password(
                    password
                ),
                role=role,
            )

            self.repository.create(user)

            self.db.commit()

            self.db.refresh(user)

            return user

        except Exception:

            self.db.rollback()

            raise

    def list_users(
        self,
        current_user,
    ):

        return (
            self.repository.list_by_tenant(
                current_user.tenant_id
            )
        )