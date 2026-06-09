from sqlalchemy.orm import Session

from src.models.tenant import Tenant


class TenantRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_company_name(
        self,
        company_name: str,
    ) -> Tenant | None:

        return (
            self.db.query(Tenant)
            .filter(
                Tenant.company_name == company_name
            )
            .first()
        )

    def create(
        self,
        tenant: Tenant,
    ) -> Tenant:

        self.db.add(tenant)

        return tenant