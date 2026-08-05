from fastapi import APIRouter, Depends, Form
from typing import Annotated

from app.core.dependencies import FormMaker
from app.core.schemas import ID

from app.security.auth.dependencies import get_current_user

from app.features.users.dependencies import get_user_service
from app.features.users.service import UserService
from app.features.users.schemas import UserIn, User as UserSchema, UserPersonal
from app.features.users.model import User as UserModel

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=ID, status_code=201)
async def create_user(user_in: Annotated[UserIn, Depends(FormMaker(UserIn))],
                      user_service: Annotated[UserService, Depends(get_user_service)]):
    user_id = await user_service.create(user_in)

    return ID(id=user_id)


@router.get('/me', response_model=UserSchema)
def read_current_user(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return current_user


@router.put('/me')
async def update_current_user(current_user: Annotated[UserModel, Depends(get_current_user)],
                              user_personal: Annotated[UserPersonal, Depends(FormMaker(UserPersonal))],
                              user_service: Annotated[UserService, Depends(get_user_service)]):
    await user_service.update_personal_data(current_user, user_personal)


@router.post('/me/username')
async def change_current_user_username(username: Annotated[str, Form()],
                                       current_user: Annotated[UserModel, Depends(get_current_user)],
                                       user_service: Annotated[UserService, Depends(get_user_service)]):
    await user_service.change_username(current_user, username)


@router.post('/me/password')
async def change_current_user_password(current_password: Annotated[str, Form()],
                                       new_password: Annotated[str, Form()],
                                       current_user: Annotated[UserModel, Depends(get_current_user)],
                                       user_service: Annotated[UserService, Depends(get_user_service)]):
    await user_service.change_password(current_user, current_password, new_password)
