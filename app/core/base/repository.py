from sqlalchemy import Select
from typing import Sequence, Any

from app.core.database.session import DBSessionWrapper


class BaseRepository:
    def __init__(self, db_session: DBSessionWrapper):
        self.__db_session = db_session

    async def _get_all(self, statement: Select) -> Sequence:
        return (await self.__db_session.execute(statement)).scalars().all()

    async def _get_one(self, statement: Select) -> Any:
        return (await self.__db_session.execute(statement)).scalar_one_or_none()
