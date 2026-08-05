from fastapi import Depends
from typing import Annotated

from app.core.dependencies import get_db_session
from app.core.database.session import DBSessionWrapper

from app.features.statuses.repository import StatusRepository
from app.features.statuses.service import StatusService


def get_status_repository(db_session: Annotated[DBSessionWrapper, Depends(get_db_session)]) -> StatusRepository:
    return StatusRepository(db_session)


def get_status_service(status_repository: Annotated[StatusRepository, Depends(get_status_repository)]) -> StatusService:
    return StatusService(status_repository)
