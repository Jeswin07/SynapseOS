from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.db.session import get_db

from src.core.rbac import (
    require_role,
)

from src.models.enums import (
    UserRole,
)

from src.modules.users.schemas import (
    CreateUserRequest,
    UserResponse,
)

from src.modules.users.service import (
    UserManagementService,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "/",
    response_model=UserResponse,
)
def create_user(
    payload: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            UserRole.ADMIN
        )
    ),
):

    try:

        service = (
            UserManagementService(db)
        )

        user = service.create_user(
            current_user=current_user,
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
            role=payload.role,
        )

        return user

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.ANALYST,
        )
    ),
):

    service = (
        UserManagementService(db)
    )

    return service.list_users(
        current_user
    )