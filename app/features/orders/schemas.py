from pydantic import BaseModel


class OrderBase(BaseModel):
    name: str
    description: str


class OrderIn(OrderBase):
    executor_id: int


class Order(OrderIn):
    id: int
    customer_id: int
    status_id: int
    is_deleted: bool
