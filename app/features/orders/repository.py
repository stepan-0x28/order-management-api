from sqlalchemy import select, update, false, Update
from sqlalchemy.sql import operators
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Sequence, Optional

from app.core.base.repository import BaseRepository

from app.features.orders.model import Order


class OrderRepository(BaseRepository):
    @staticmethod
    def __build_order_update(order_id: int) -> Update:
        return update(Order).where(Order.id == order_id)

    async def __get_orders(self,
                           user_column: InstrumentedAttribute,
                           user_id: int,
                           include_deleted: bool) -> Sequence[Order]:
        statement = select(Order).where(operators.eq(user_column, user_id))

        if not include_deleted:
            statement = statement.where(Order.is_deleted == false())

        return await self._get_all(statement)

    async def __get_order(self, user_column: InstrumentedAttribute, user_id: int, order_id: int) -> Optional[Order]:
        statement = (
            select(Order)
            .where(operators.eq(user_column, user_id))
            .where(Order.id == order_id)
            .where(Order.is_deleted == false())
        )

        return await self._get_one(statement)

    async def get_customer_orders(self, customer_id: int, include_deleted: bool) -> Sequence[Order]:
        return await self.__get_orders(Order.customer_id, customer_id, include_deleted)

    async def get_executor_orders(self, executor_id: int, include_deleted: bool) -> Sequence[Order]:
        return await self.__get_orders(Order.executor_id, executor_id, include_deleted)

    async def get_customer_order(self, customer_id: int, order_id: int) -> Optional[Order]:
        return await self.__get_order(Order.customer_id, customer_id, order_id)

    async def get_executor_order(self, executor_id: int, order_id: int) -> Optional[Order]:
        return await self.__get_order(Order.executor_id, executor_id, order_id)

    async def update_base(self, order_id: int, name: str, description: str):
        await self.execute(self.__build_order_update(order_id).values(name=name, description=description))

    async def change_executor(self, order_id: int, executor_id: int):
        await self.execute(self.__build_order_update(order_id).values(executor_id=executor_id))

    async def change_status(self, order_id: int, status_id: int):
        await self.execute(self.__build_order_update(order_id).values(status_id=status_id))

    async def mark_deleted(self, order_id: int):
        await self.execute(self.__build_order_update(order_id).values(is_deleted=True))
