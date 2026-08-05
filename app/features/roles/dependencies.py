from typing import Annotated
from fastapi import Depends

from app.core.dependencies import get_db_session
from app.core.database.session import SessionWrapper

from app.features.roles.repository import RoleRepository
from app.features.roles.service import RoleService


def get_role_repository(db_session: Annotated[SessionWrapper, Depends(get_db_session)]) -> RoleRepository:
    return RoleRepository(db_session)


def get_role_service(role_repository: Annotated[RoleRepository, Depends(get_role_repository)]) -> RoleService:
    return RoleService(role_repository)
