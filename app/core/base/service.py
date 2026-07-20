from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Callable, Awaitable

from app.core.database.exceptions import convert_integrity_error


class BaseService:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def __execute_session_method(self, session_method: Callable[[], Awaitable]):
        try:
            await session_method()
        except IntegrityError as err:
            raise convert_integrity_error(self.__session.get_bind().dialect.name, err)

    async def flush(self):
        await self.__execute_session_method(self.__session.flush)

    async def commit(self):
        await self.__execute_session_method(self.__session.commit)
