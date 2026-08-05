from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Executable, Result

from app.core.base.model import BaseModel
from app.core.database.exceptions import convert_integrity_error


class SessionWrapper:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def commit(self):
        try:
            await self.__db_session.commit()
        except IntegrityError as err:
            raise convert_integrity_error(self.__db_session.get_bind().dialect.name, err)

    async def execute(self, statement: Executable) -> Result:
        return await self.__db_session.execute(statement)

    def add(self, model: BaseModel):
        self.__db_session.add(model)
