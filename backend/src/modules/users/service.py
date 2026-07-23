import logging

from sqlalchemy.orm import Session

from src.models.user import User
from src.modules.auth.security import (
    hash_password,
)
from src.modules.users.repository import (
    UserManagementRepository,
)

logger = logging.getLogger(__name__)

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

        logger.info(
            "User creation started | tenant_id=%s email=%s role=%s requested_by=%s",
            current_user.tenant_id,
            email,
            role,
            current_user.id,
        )

        existing_user = (
            self.repository.get_by_email(email)
        )

        if existing_user:
            logger.warning(
                "User creation rejected | tenant_id=%s email=%s reason=already_exists",
                current_user.tenant_id,
                email,
            )
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

            logger.info(
                "User created | user_id=%s tenant_id=%s role=%s created_by=%s",
                user.id,
                user.tenant_id,
                user.role,
                current_user.id,
            )

            return user

        except Exception:

            self.db.rollback()

            raise

    def list_users(
        self,
        current_user,
    ):

        logger.info(
            "User list requested | tenant_id=%s requested_by=%s",
            current_user.tenant_id,
            current_user.id,
        )

        return (
            self.repository.list_by_tenant(
                current_user.tenant_id
            )
        )