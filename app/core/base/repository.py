from sqlalchemy import Select, Result, Executable
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Any

from app.core.base.model import BaseModel


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def _get_all(self, statement: Select) -> Sequence:
        return (await self.execute(statement)).scalars().all()

    async def _get_one(self, statement: Select) -> Any:
        return (await self.execute(statement)).scalar_one_or_none()

    def add(self, model: BaseModel):
        self.__session.add(model)

    async def execute(self, statement: Executable) -> Result:
        return await self.__session.execute(statement)
