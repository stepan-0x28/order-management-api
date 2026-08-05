from typing import Sequence

from app.features.roles.repository import RoleRepository
from app.features.roles.model import Role


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.__role_repository = role_repository

    async def get_all(self) -> Sequence[Role]:
        return await self.__role_repository.get_all()
