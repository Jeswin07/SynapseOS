from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.db.session import get_db

from src.modules.tenants.schemas import (
    TenantCreate,
)

from src.modules.tenants.service import (
    TenantService,
)

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)

@router.post("/")
def create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db),
):

    try:

        service = TenantService(db)

        tenant = service.create_tenant(
            company_name=payload.company_name,
            industry=payload.industry,
        )

        db.commit()

        return {
            "tenant_id": str(tenant.id),
            "company_name": tenant.company_name,
        }

    except ValueError as exc:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    