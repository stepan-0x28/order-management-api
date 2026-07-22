from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_session

from app.features.roles.service import RoleService


def get_role_service(session: Annotated[AsyncSession, Depends(get_session)]) -> RoleService:
    return RoleService(session)
