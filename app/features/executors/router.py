from fastapi import APIRouter, Depends
from typing import Annotated

from app.features.executors.dependencies import get_executor_service
from app.features.executors.service import ExecutorService
from app.features.users.schemas import UserOut

router = APIRouter(prefix='/executors', tags=['executors'])


@router.get('', response_model=list[UserOut])
async def read_executors(executor_service: Annotated[ExecutorService, Depends(get_executor_service)]):
    return await executor_service.get_all()
