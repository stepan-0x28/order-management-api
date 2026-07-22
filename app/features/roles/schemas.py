from pydantic import BaseModel


class Role(BaseModel):
    id: int
    key: str
    name: str
    description: str
