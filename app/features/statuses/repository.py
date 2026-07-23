from sqlalchemy import select
from typing import Optional, Sequence

from app.core.base.repository import BaseRepository

from app.features.statuses.model import Status


class StatusRepository(BaseRepository):
    async def get_all(self) -> Sequence[Status]:
        return await self._get_all(select(Status))

    async def get_by_id(self, status_id: int) -> Optional[Status]:
        return await self._get_one(select(Status).where(Status.id == status_id))

    async def get_by_key(self, key: str) -> Optional[Status]:
        return await self._get_one(select(Status).where(Status.key == key))
