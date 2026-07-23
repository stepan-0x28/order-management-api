from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.statuses.repository import StatusRepository
from app.features.statuses.model import Status


class StatusService:
    def __init__(self, session: AsyncSession):
        self.__status_repository = StatusRepository(session)

    async def get_all(self) -> Sequence[Status]:
        return await self.__status_repository.get_all()
