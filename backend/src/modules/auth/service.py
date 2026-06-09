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

from src.modules.tenants.service import (
    TenantService,
)


class AuthService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = UserRepository(db)

        self.tenant_service = TenantService(db)

    def register(
        self,
        company_name: str,
        industry: str,
        full_name: str,
        email: str,
        password: str,
    ):

        try:

            existing_user = (
                self.repository.get_by_email(email)
            )

            if existing_user:
                raise ValueError(
                    "User already exists"
                )

            tenant = (
                self.tenant_service.create_tenant(
                    company_name=company_name,
                    industry=industry,
                )
            )

            user = User(
                tenant_id=tenant.id,
                email=email,
                full_name=full_name,
                hashed_password=hash_password(
                    password
                ),
                role=UserRole.ADMIN,
            )

            self.repository.create(user)

            self.db.commit()

            self.db.refresh(tenant)
            self.db.refresh(user)

            return {
                "tenant": tenant,
                "user": user,
            }

        except Exception:

            self.db.rollback()

            raise

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