from sqlalchemy import select
from typing import Optional

from app.core.base.repository import BaseRepository

from app.features.users.model import User


class UserRepository(BaseRepository):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self._get_one(select(User).where(User.id == user_id))

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self._get_one(select(User).where(User.username == username))
