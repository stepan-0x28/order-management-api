from sqlalchemy import select, update, Update
from typing import Optional

from app.core.base.repository import BaseRepository

from app.features.users.model import User


class UserRepository(BaseRepository):
    @staticmethod
    def __build_user_update(user_id: int) -> Update:
        return update(User).where(User.id == user_id)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._get_one(select(User).where(User.id == user_id))

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self._get_one(select(User).where(User.username == username))

    async def update_data(self, user_id: int, first_name: str, last_name: str):
        await self.execute(self.__build_user_update(user_id).values(first_name=first_name, last_name=last_name))

    async def update_username(self, user_id: int, username: str):
        await self.execute(self.__build_user_update(user_id).values(username=username))

    async def update_password_hash(self, user_id: int, password_hash: str):
        await self.execute(self.__build_user_update(user_id).values(password_hash=password_hash))

    async def increase_token_version(self, user_id: int):
        await self.execute(self.__build_user_update(user_id).values(token_version=User.token_version + 1))
