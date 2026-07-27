from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.core.base.service import BaseService
from app.core.database.exceptions import ForeignKeyViolationError

from app.features.orders.exceptions import NonExistentOrderError, SameStatusError
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


class OrderService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.__order_repository = OrderRepository(session)
        self.__status_repository = StatusRepository(session)
        self.__executor_repository = ExecutorRepository(session)

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

        self.__order_repository.add(order)

        try:
            await self.flush()

            order_id = order.id

            await self.commit()
        except ForeignKeyViolationError:
            raise NonExistentExecutorError

        return order_id

    async def get_all(self, user: User, include_deleted: bool = False) -> Sequence[Order]:
        if await user.has_role(Role.EXECUTOR):
            return await self.__order_repository.get_executor_orders(user.id, include_deleted)

        return await self.__order_repository.get_customer_orders(user.id, include_deleted)

    async def update_base(self, customer: User, order_id: int, order_base: OrderBase):
        if await self.__order_repository.get_customer_order(customer.id, order_id) is None:
            raise NonExistentOrderError

        await self.__order_repository.update_base(order_id, order_base.name, order_base.description)

        await self.commit()

    async def change_executor(self, customer: User, order_id: int, executor_id: int):
        if await self.__order_repository.get_customer_order(customer.id, order_id) is None:
            raise NonExistentOrderError

        if await self.__executor_repository.get_by_id(executor_id) is None:
            raise NonExistentExecutorError

        await self.__order_repository.change_executor(order_id, executor_id)

        try:
            await self.commit()
        except ForeignKeyViolationError:
            raise NonExistentExecutorError

    async def change_status(self, user: User, order_id: int, status_id: int):
        if await user.has_role(Role.EXECUTOR):
            order = await self.__order_repository.get_executor_order(user.id, order_id)
        else:
            order = await self.__order_repository.get_customer_order(user.id, order_id)

        if order is None:
            raise NonExistentOrderError

        if order.status_id == status_id:
            raise SameStatusError

        if await self.__status_repository.get_by_id(status_id) is None:
            raise NonExistentStatusError

        await self.__order_repository.change_status(order_id, status_id)

        try:
            await self.commit()
        except ForeignKeyViolationError:
            raise NonExistentStatusError

    async def mark_deleted(self, customer: User, order_id: int):
        if await self.__order_repository.get_customer_order(customer.id, order_id) is None:
            raise NonExistentOrderError

        await self.__order_repository.mark_deleted(order_id)

        await self.commit()
