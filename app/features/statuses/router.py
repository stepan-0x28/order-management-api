from fastapi import APIRouter, Depends
from typing import Annotated

from app.features.statuses.dependencies import get_status_service
from app.features.statuses.service import StatusService
from app.features.statuses.schemas import Status

router = APIRouter(prefix='/statuses', tags=['statuses'])


@router.get('', response_model=list[Status])
async def read_statuses(status_service: Annotated[StatusService, Depends(get_status_service)]):
    return await status_service.get_all()
