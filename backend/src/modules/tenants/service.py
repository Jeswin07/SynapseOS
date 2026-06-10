from sqlalchemy.orm import Session

from src.models.tenant import Tenant
from src.modules.tenants.repository import (
    TenantRepository,
)


class TenantService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = TenantRepository(db)

    def create_tenant(
        self,
        company_name: str,
        industry: str,
    ) -> Tenant:

        existing = self.repository.get_by_company_name(company_name)

        if existing:
            raise ValueError("Company already exists")

        tenant = Tenant(
            company_name=company_name,
            industry=industry,
        )

        self.repository.create(tenant)

        self.db.flush()

        return tenant
