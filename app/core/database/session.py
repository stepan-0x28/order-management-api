from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Executable, Result

from app.core.base.model import BaseModel
from app.core.database.exceptions import convert_integrity_error


class SessionWrapper:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def commit(self):
        try:
            await self.__session.commit()
        except IntegrityError as err:
            raise convert_integrity_error(self.__session.get_bind().dialect.name, err)

    async def execute(self, statement: Executable) -> Result:
        return await self.__session.execute(statement)

    def add(self, model: BaseModel):
        self.__session.add(model)
