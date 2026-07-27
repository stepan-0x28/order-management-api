from typing import Annotated
from fastapi import Depends

from app.security.auth.dependencies import get_current_user

from app.features.roles.exceptions import InappropriateRoleError
from app.features.roles.enums import Role
from app.features.users.model import User


async def get_current_customer(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not await current_user.has_role(Role.CUSTOMER):
        raise InappropriateRoleError

    return current_user
