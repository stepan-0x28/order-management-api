from typing import AsyncGenerator
from fastapi import Form
from pydantic import BaseModel
from inspect import Signature, Parameter

from app.core.database.connection import async_session_maker
from app.core.database.session import SessionWrapper


async def get_db_session() -> AsyncGenerator[SessionWrapper, None]:
    async with async_session_maker() as db_session:
        yield SessionWrapper(db_session)


class FormMaker:
    def __init__(self, model_class: type[BaseModel]):
        self.__model_class = model_class

        self.__signature__ = Signature(
            [
                Parameter(
                    name=name,
                    kind=Parameter.KEYWORD_ONLY,
                    default=Form(...),
                    annotation=info.annotation
                ) for name, info in self.__model_class.model_fields.items()
            ]
        )

    def __call__(self, **kwargs) -> BaseModel:
        return self.__model_class(**kwargs)
