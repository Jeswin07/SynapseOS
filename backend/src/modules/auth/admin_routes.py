from fastapi import (
    APIRouter,
    Depends,
)

from src.core.rbac import (
    require_role,
)
from src.models.enums import (
    UserRole,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user=Depends(require_role(UserRole.ADMIN)),
):

    return {"message": "Admin Access Granted"}


@router.get("/analytics")
def analytics_dashboard(
    current_user=Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.ANALYST,
        )
    ),
):

    return {"message": "Analytics Access Granted"}
