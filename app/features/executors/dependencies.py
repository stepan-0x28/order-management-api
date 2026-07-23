from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session

from app.features.executors.service import ExecutorService


def get_executor_service(session: Annotated[AsyncSession, Depends(get_session)]) -> ExecutorService:
    return ExecutorService(session)
