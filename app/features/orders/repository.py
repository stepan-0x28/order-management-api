from sqlalchemy import select, false, Select
from sqlalchemy.sql import operators
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Sequence, Optional

from app.core.base.repository import BaseRepository

from app.features.orders.model import Order


class OrderRepository(BaseRepository):
    @staticmethod
    def __build_base_user_orders_select(user_column: InstrumentedAttribute, user_id: int) -> Select:
        return select(Order).where(operators.eq(user_column, user_id))

    def __build_user_orders_select(self,
                                   user_column: InstrumentedAttribute,
                                   user_id: int,
                                   include_deleted: bool) -> Select:
        statement = self.__build_base_user_orders_select(user_column, user_id)

        if not include_deleted:
            statement = statement.where(Order.is_deleted == false())

        return statement

    def __build_user_order_select(self, user_column: InstrumentedAttribute, user_id: int, order_id: int) -> Select:
        statement = (
            self.__build_base_user_orders_select(user_column, user_id)
            .where(Order.id == order_id)
            .where(Order.is_deleted == false())
        )

        return statement

    async def get_customer_orders(self, customer_id: int, include_deleted: bool) -> Sequence[Order]:
        return await self._get_all(self.__build_user_orders_select(Order.customer_id, customer_id, include_deleted))

    async def get_executor_orders(self, executor_id: int, include_deleted: bool) -> Sequence[Order]:
        return await self._get_all(self.__build_user_orders_select(Order.executor_id, executor_id, include_deleted))

    async def get_customer_order(self, customer_id: int, order_id: int) -> Optional[Order]:
        return await self._get_one(self.__build_user_order_select(Order.customer_id, customer_id, order_id))

    async def get_executor_order(self, executor_id: int, order_id: int) -> Optional[Order]:
        return await self._get_one(self.__build_user_order_select(Order.executor_id, executor_id, order_id))
