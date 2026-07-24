from pydantic import BaseModel


class UserPersonal(BaseModel):
    first_name: str
    last_name: str


class UserIn(UserPersonal):
    password: str
    username: str
    role_id: int


class UserOut(UserPersonal):
    id: int
    username: str
    role_id: int
