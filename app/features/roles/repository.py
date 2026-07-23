from sqlalchemy import select
from typing import Optional, Sequence

from app.core.base.repository import BaseRepository

from app.features.roles.model import Role


class RoleRepository(BaseRepository):
    async def get_all(self) -> Sequence[Role]:
        return await self._get_all(select(Role))

    async def get_by_id(self, role_id: int) -> Optional[Role]:
        return await self._get_one(select(Role).where(Role.id == role_id))
