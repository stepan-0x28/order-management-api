from typing import Annotated
from fastapi import Depends

from app.security.auth.dependencies import get_current_user

from app.features.roles.exceptions import InappropriateRoleError
from app.features.roles.enums import Role
from app.features.users.model import User


async def get_current_customer(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if (await current_user.awaitable_attrs.role).key != Role.CUSTOMER:
        raise InappropriateRoleError

    return current_user
