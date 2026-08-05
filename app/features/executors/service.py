from typing import Sequence

from app.features.executors.repository import ExecutorRepository
from app.features.users.model import User


class ExecutorService:
    def __init__(self, executor_repository: ExecutorRepository):
        self.__executor_repository = executor_repository

    async def get_all(self) -> Sequence[User]:
        return await self.__executor_repository.get_all()
