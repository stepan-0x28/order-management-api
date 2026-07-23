from sqlalchemy import select, Select
from typing import Optional, Sequence

from app.core.base.repository import BaseRepository

from app.features.roles.enums import Roles
from app.features.roles.model import Role
from app.features.users.model import User


class ExecutorRepository(BaseRepository):
    @staticmethod
    def __build_executors_select() -> Select:
        return select(User).join(User.role).where(Role.key == Roles.EXECUTOR)

    async def get_all(self) -> Sequence[User]:
        return await self._get_all(self.__build_executors_select())

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._get_one(self.__build_executors_select().where(User.id == user_id))
