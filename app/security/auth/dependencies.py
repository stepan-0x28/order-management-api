from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.security.auth.service import AuthService

from app.features.users.model import User
from app.features.users.dependencies import get_user_repository
from app.features.users.repository import UserRepository

_oauth2_scheme = OAuth2PasswordBearer('/auth/login')


def get_auth_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(user_repository)


async def get_current_user(token: Annotated[str, Depends(_oauth2_scheme)],
                           auth_service: Annotated[AuthService, Depends(get_auth_service)]) -> User:
    return await auth_service.get_user(token)
