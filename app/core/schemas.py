from pydantic import BaseModel


class IDResponse(BaseModel):
    id: int
