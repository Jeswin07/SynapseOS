from sqlalchemy.orm import Session

from src.models.enums import UserRole
from src.models.user import User
from src.modules.auth.repository import UserRepository
from src.modules.auth.security import (
    hash_password,
    verify_password,
)
from src.modules.tenants.service import (
    TenantService,
)
from src.modules.auth.refresh_token_repository import (
    RefreshTokenRepository,
)
from datetime import (
    UTC,
    datetime,
    timedelta,
)

from src.core.config import settings

from src.models.refresh_token import (
    RefreshToken,
)

from src.modules.auth.token_service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    is_refresh_token,
)


class AuthService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = UserRepository(db)

        self.tenant_service = TenantService(db)

        self.refresh_repository = RefreshTokenRepository(db)

    def register(
        self,
        company_name: str,
        industry: str,
        full_name: str,
        email: str,
        password: str,
    ):

        try:
            existing_user = self.repository.get_by_email(email)

            if existing_user:
                raise ValueError("User already exists")

            tenant = self.tenant_service.create_tenant(
                company_name=company_name,
                industry=industry,
            )

            user = User(
                tenant_id=tenant.id,
                email=email,
                full_name=full_name,
                hashed_password=hash_password(password),
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

        user = self.repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid credentials")

        try:
            access_token = create_access_token(
                str(user.id),
                str(user.tenant_id),
                user.role.value,
            )

            refresh_token = create_refresh_token(
                str(user.id),
            )

            refresh_token_record = RefreshToken(
                user_id=user.id,
                token=refresh_token,
                expires_at=(
                    datetime.now(UTC)
                    + timedelta(days=settings.refresh_token_expire_days)
                ),
            )

            self.refresh_repository.create(refresh_token_record)

            self.db.commit()

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user,
            }

        except Exception:
            self.db.rollback()

            raise

    def refresh_access_token(
        self,
        refresh_token: str,
    ):

        payload = decode_token(refresh_token)

        if not is_refresh_token(payload):
            raise ValueError("Invalid refresh token")

        stored_token = self.refresh_repository.get_by_token(refresh_token)

        if not stored_token:
            raise ValueError("Refresh token not found")

        if stored_token.expires_at < datetime.utcnow():
            raise ValueError("Refresh token expired")

        user = self.repository.get_by_id(str(stored_token.user_id))

        if not user:
            raise ValueError("User not found")

        access_token = create_access_token(
            str(user.id),
            str(user.tenant_id),
            user.role.value,
        )

        return access_token
    

    def logout(
        self,
        refresh_token: str,
    ):

        stored_token = (
            self.refresh_repository.get_by_token(
                refresh_token
            )
        )

        if not stored_token:
            raise ValueError(
                "Refresh token not found"
            )

        try:

            self.refresh_repository.delete_by_token(
                refresh_token
            )

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise
