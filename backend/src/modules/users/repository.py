from sqlalchemy.orm import Session

from src.models.user import User


class UserManagementRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)

        return user

    def list_by_tenant(
        self,
        tenant_id,
    ):

        return (
            self.db.query(User)
            .filter(
                User.tenant_id == tenant_id
            )
            .all()
        )