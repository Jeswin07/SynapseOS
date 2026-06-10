from fastapi import (
    Depends,
    HTTPException,
)

from src.core.security import (
    get_current_user,
)
from src.models.enums import (
    UserRole,
)


def require_role(
    *allowed_roles: UserRole,
):

    def role_checker(
        current_user=Depends(get_current_user),
    ):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker
