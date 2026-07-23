import logging

from sqlalchemy.orm import Session

from src.models.tenant import Tenant
from src.modules.tenants.repository import (
    TenantRepository,
)

logger = logging.getLogger(__name__)

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

        logger.info(
            "Tenant creation started | company=%s industry=%s",
            company_name,
            industry,
        )

        existing = self.repository.get_by_company_name(company_name)

        if existing:
            logger.warning(
                "Tenant creation rejected | company=%s reason=already_exists",
                company_name,
            )
            raise ValueError("Company already exists")

        tenant = Tenant(
            company_name=company_name,
            industry=industry,
        )

        self.repository.create(tenant)

        self.db.flush()

        logger.info(
            "Tenant created | tenant_id=%s company=%s",
            tenant.id,
            tenant.company_name,
        )

        return tenant
