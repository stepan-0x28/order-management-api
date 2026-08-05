from fastapi import APIRouter, Depends, Form
from typing import Annotated

from app.core.dependencies import FormMaker
from app.core.schemas import ID

from app.security.auth.dependencies import get_current_user
from app.security.authz.dependencies import get_current_customer

from app.features.orders.dependencies import get_order_service
from app.features.orders.service import OrderService
from app.features.orders.schemas import OrderIn, Order, OrderBase
from app.features.users.model import User

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('', response_model=ID, status_code=201)
async def create_order(order_service: Annotated[OrderService, Depends(get_order_service)],
                       current_customer: Annotated[User, Depends(get_current_customer)],
                       order_in: Annotated[OrderIn, Depends(FormMaker(OrderIn))]):
    order_id = await order_service.create(current_customer, order_in)

    return ID(id=order_id)


@router.get('', response_model=list[Order])
async def get_orders(current_user: Annotated[User, Depends(get_current_user)],
                     order_service: Annotated[OrderService, Depends(get_order_service)],
                     include_deleted: bool = False):
    return await order_service.get_all(current_user, include_deleted)


@router.put('/{order_id}')
async def update_order(current_customer: Annotated[User, Depends(get_current_customer)],
                       order_id: int,
                       order_service: Annotated[OrderService, Depends(get_order_service)],
                       order_base: Annotated[OrderBase, Depends(FormMaker(OrderBase))]):
    await order_service.update_base_data(current_customer, order_id, order_base)


@router.post('/{order_id}/status')
async def change_status(current_user: Annotated[User, Depends(get_current_user)],
                        order_id: int,
                        status_id: Annotated[int, Form()],
                        order_service: Annotated[OrderService, Depends(get_order_service)]):
    await order_service.change_status(current_user, order_id, status_id)


@router.post('/{order_id}/executor')
async def change_executor(current_customer: Annotated[User, Depends(get_current_customer)],
                          order_id: int,
                          order_service: Annotated[OrderService, Depends(get_order_service)],
                          executor_id: Annotated[int, Form()]):
    await order_service.change_executor(current_customer, order_id, executor_id)


@router.delete('/{order_id}')
async def delete_order(current_customer: Annotated[User, Depends(get_current_customer)],
                       order_id: int,
                       order_service: Annotated[OrderService, Depends(get_order_service)]):
    await order_service.mark_deleted(current_customer, order_id)
