from fastapi import APIRouter, Depends
from typing import Annotated

from app.features.roles.dependencies import get_role_service
from app.features.roles.service import RoleService
from app.features.roles.schemas import Role

router = APIRouter(prefix='/roles', tags=['roles'])


@router.get('', response_model=list[Role])
async def read_roles(role_service: Annotated[RoleService, Depends(get_role_service)]):
    return await role_service.get_all()
