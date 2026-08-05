from fastapi import Depends
from typing import Annotated

from app.core.dependencies import get_db_session
from app.core.database.session import SessionWrapper

from app.features.users.repository import UserRepository
from app.features.users.service import UserService
from app.features.roles.repository import RoleRepository
from app.features.roles.dependencies import get_role_repository


def get_user_repository(session: Annotated[SessionWrapper, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(session)


def get_user_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)],
                     role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
                     session: Annotated[SessionWrapper, Depends(get_db_session)]) -> UserService:
    return UserService(user_repository, role_repository, session)
