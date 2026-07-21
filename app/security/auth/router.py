from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.security.auth.dependencies import get_auth_service
from app.security.auth.service import AuthService
from app.security.auth.schemas import Token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    token = await auth_service.create_token(form_data.username, form_data.password)

    return Token(access_token=token)
