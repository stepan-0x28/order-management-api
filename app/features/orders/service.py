from typing import Sequence

from app.core.database.session import SessionWrapper

from app.features.orders.exceptions import NonExistentOrderError, SameStatusError, SameExecutorError
from app.features.orders.repository import OrderRepository
from app.features.orders.schemas import OrderBase, OrderIn
from app.features.orders.model import Order
from app.features.roles.enums import Role
from app.features.executors.exceptions import NonExistentExecutorError
from app.features.executors.repository import ExecutorRepository
from app.features.users.model import User
from app.features.statuses.exceptions import NonExistentStatusError
from app.features.statuses.enums import Status
from app.features.statuses.repository import StatusRepository


class OrderService:
    def __init__(self,
                 order_repository: OrderRepository,
                 status_repository: StatusRepository,
                 executor_repository: ExecutorRepository,
                 session: SessionWrapper):
        self.__order_repository = order_repository
        self.__status_repository = status_repository
        self.__executor_repository = executor_repository

        self.__session = session

    async def create(self, customer: User, order_in: OrderIn) -> int:
        if await self.__executor_repository.get_by_id(order_in.executor_id) is None:
            raise NonExistentExecutorError

        status = await self.__status_repository.get_by_key(Status.NEW)

        order = Order(
            customer_id=customer.id,
            status_id=status.id,
            name=order_in.name,
            description=order_in.description,
            executor_id=order_in.executor_id
        )

        self.__session.add(order)

        await self.__session.commit()

        return order.id

    async def get_all(self, user: User, include_deleted: bool = False) -> Sequence[Order]:
        if await user.is_role(Role.EXECUTOR):
            return await self.__order_repository.get_executor_orders(user.id, include_deleted)

        return await self.__order_repository.get_customer_orders(user.id, include_deleted)

    async def update_base_data(self, customer: User, order_id: int, order_base: OrderBase):
        order = await self.__order_repository.get_customer_order(customer.id, order_id)

        if order is None:
            raise NonExistentOrderError

        order.name = order_base.name
        order.description = order_base.description

        await self.__session.commit()

    async def change_executor(self, customer: User, order_id: int, executor_id: int):
        order = await self.__order_repository.get_customer_order(customer.id, order_id)

        if order is None:
            raise NonExistentOrderError

        if order.executor_id == executor_id:
            raise SameExecutorError

        if await self.__executor_repository.get_by_id(executor_id) is None:
            raise NonExistentExecutorError

        order.executor_id = executor_id

        await self.__session.commit()

    async def change_status(self, user: User, order_id: int, status_id: int):
        if await user.is_role(Role.EXECUTOR):
            order = await self.__order_repository.get_executor_order(user.id, order_id)
        else:
            order = await self.__order_repository.get_customer_order(user.id, order_id)

        if order is None:
            raise NonExistentOrderError

        if order.status_id == status_id:
            raise SameStatusError

        if await self.__status_repository.get_by_id(status_id) is None:
            raise NonExistentStatusError

        order.status_id = status_id

        await self.__session.commit()

    async def mark_deleted(self, customer: User, order_id: int):
        order = await self.__order_repository.get_customer_order(customer.id, order_id)

        if order is None:
            raise NonExistentOrderError

        order.is_deleted = True

        await self.__session.commit()
