from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from backend.app.core.auth import get_current_user
from backend.app.models.user import User


def require_roles(*allowed_roles: str) -> Callable[[User], User]:
    """Return a dependency that enforces server-side role permissions."""

    def authorize(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return authorize
