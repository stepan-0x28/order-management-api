from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from app.core.base.model import BaseModel


class Status(BaseModel):
    __tablename__ = 'statuses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
