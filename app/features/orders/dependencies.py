from fastapi import Depends
from typing import Annotated

from app.core.dependencies import get_db_session
from app.core.database.session import SessionWrapper

from app.features.orders.repository import OrderRepository
from app.features.orders.service import OrderService
from app.features.statuses.repository import StatusRepository
from app.features.statuses.dependencies import get_status_repository
from app.features.executors.repository import ExecutorRepository
from app.features.executors.dependencies import get_executor_repository


def get_order_repository(db_session: Annotated[SessionWrapper, Depends(get_db_session)]) -> OrderRepository:
    return OrderRepository(db_session)


def get_order_service(order_repository: Annotated[OrderRepository, Depends(get_order_repository)],
                      status_repository: Annotated[StatusRepository, Depends(get_status_repository)],
                      executor_repository: Annotated[ExecutorRepository, Depends(get_executor_repository)],
                      db_session: Annotated[SessionWrapper, Depends(get_db_session)]) -> OrderService:
    return OrderService(order_repository, status_repository, executor_repository, db_session)
