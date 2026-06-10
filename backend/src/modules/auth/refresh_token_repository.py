from sqlalchemy.orm import Session

from src.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:

        self.db.add(refresh_token)

        return refresh_token

    def get_by_token(
        self,
        token: str,
    ) -> RefreshToken | None:

        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def delete(
        self,
        refresh_token: RefreshToken,
    ):

        self.db.delete(refresh_token)

    def delete_by_token(
        self,
        token: str,
    ):

        refresh_token = (
            self.get_by_token(token)
        )

        if refresh_token:
            self.db.delete(refresh_token)
