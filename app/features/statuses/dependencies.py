from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.dependencies import get_session

from app.features.statuses.service import StatusService


def get_status_service(session: Annotated[AsyncSession, Depends(get_session)]) -> StatusService:
    return StatusService(session)
