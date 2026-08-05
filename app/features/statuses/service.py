from typing import Sequence

from app.features.statuses.repository import StatusRepository
from app.features.statuses.model import Status


class StatusService:
    def __init__(self, status_repository: StatusRepository):
        self.__status_repository = status_repository

    async def get_all(self) -> Sequence[Status]:
        return await self.__status_repository.get_all()
