from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.features.executors.repository import ExecutorRepository
from app.features.users.model import User


class ExecutorService:
    def __init__(self, session: AsyncSession):
        self.__executor_repository = ExecutorRepository(session)

    async def get_all(self) -> Sequence[User]:
        return await self.__executor_repository.get_all()
