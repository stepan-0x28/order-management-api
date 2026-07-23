from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.roles.repository import RoleRepository
from app.features.roles.model import Role


class RoleService:
    def __init__(self, session: AsyncSession):
        self.__role_repository = RoleRepository(session)

    async def get_all(self) -> Sequence[Role]:
        return await self.__role_repository.get_all()
