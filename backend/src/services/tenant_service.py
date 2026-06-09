from sqlalchemy.orm import Session

from src.repositories.tenant_repository import TenantRepository


class TenantService:

    def __init__(self, db: Session):
        self.repository = TenantRepository(db)

    def create_tenant(
        self,
        company_name: str,
        industry: str
    ):
        return self.repository.create(
            company_name,
            industry
        )