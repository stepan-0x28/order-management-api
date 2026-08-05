from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, text

from app.core.base.model import BaseModel

from app.features.roles.model import Role


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    token_version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))

    role: Mapped[Role] = relationship(Role)

    async def is_role(self, role_key: str) -> bool:
        role = await self.awaitable_attrs.role

        return role.key == role_key
