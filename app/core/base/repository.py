from sqlalchemy import Select
from typing import Sequence, Any

from app.core.database.session import SessionWrapper


class BaseRepository:
    def __init__(self, session: SessionWrapper):
        self.__session = session

    async def _get_all(self, statement: Select) -> Sequence:
        return (await self.__session.execute(statement)).scalars().all()

    async def _get_one(self, statement: Select) -> Any:
        return (await self.__session.execute(statement)).scalar_one_or_none()
