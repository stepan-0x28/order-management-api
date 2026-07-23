from pydantic import BaseModel


class Status(BaseModel):
    id: int
    key: str
    name: str
    description: str
