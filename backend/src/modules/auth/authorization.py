from collections.abc import Callable

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from src.models.enums import UserRole
from src.modules.auth.dependencies import (
    get_current_user,
)


def require_roles(
    *roles: UserRole,
) -> Callable:
    """
    Require one of the specified roles.

    Args:
        roles: Allowed user roles.

    Returns:
        Dependency callable.
    """

    def checker(
        current_user=Depends(
            get_current_user,
        ),
    ):

        if current_user.role not in roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )

        return current_user

    return checker