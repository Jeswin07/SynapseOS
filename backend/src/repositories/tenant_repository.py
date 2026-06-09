from sqlalchemy.orm import Session

from src.models.tenant import Tenant


class TenantRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        company_name: str,
        industry: str
    ) -> Tenant:

        tenant = Tenant(
            company_name=company_name,
            industry=industry
        )

        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)

        return tenant