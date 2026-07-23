from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session

from app.security.auth.service import AuthService

from app.features.users.model import User

_oauth2_scheme = OAuth2PasswordBearer('/auth/login')


def get_auth_service(session: Annotated[AsyncSession, Depends(get_session)]) -> AuthService:
    return AuthService(session)


async def get_current_user(token: Annotated[str, Depends(_oauth2_scheme)],
                           auth_service: Annotated[AuthService, Depends(get_auth_service)]) -> User:
    return await auth_service.get_user(token)
