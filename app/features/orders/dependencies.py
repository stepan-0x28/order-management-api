from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session

from app.features.orders.service import OrderService


def get_order_service(session: Annotated[AsyncSession, Depends(get_session)]) -> OrderService:
    return OrderService(session)
