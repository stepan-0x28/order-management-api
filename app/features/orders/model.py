from sqlalchemy import Integer, String, ForeignKey, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base.model import BaseModel

from app.features.users.model import User
from app.features.statuses.model import Status


class Order(BaseModel):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    executor_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))

    customer: Mapped[User] = relationship(User, foreign_keys=[customer_id])
    executor: Mapped[User] = relationship(User, foreign_keys=[executor_id])
    status: Mapped[Status] = relationship(Status)
