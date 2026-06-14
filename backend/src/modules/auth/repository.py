from sqlalchemy.orm import Session

from src.models.user import User


class UserRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return self.db.query(User).filter(User.email == email).first()

    def create(
        self,
        user: User,
    ) -> User:

        self.db.add(user)

        return user

    import uuid

    def get_by_id(
        self,
        user_id: uuid.UUID,
    ) -> User | None:
        """
        Retrieve a user by ID.

        Args:
            user_id: User UUID.

        Returns:
            User instance if found, otherwise None.
        """

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )
