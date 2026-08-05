from fastapi import Depends
from typing import Annotated

from app.core.dependencies import get_db_session
from app.core.database.session import DBSessionWrapper

from app.features.executors.repository import ExecutorRepository
from app.features.executors.service import ExecutorService


def get_executor_repository(db_session: Annotated[DBSessionWrapper, Depends(get_db_session)]) -> ExecutorRepository:
    return ExecutorRepository(db_session)


def get_executor_service(executor_repository: Annotated[ExecutorRepository, Depends(get_executor_repository)]
                         ) -> ExecutorService:
    return ExecutorService(executor_repository)
