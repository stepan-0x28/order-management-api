from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect

from app.features.roles.model import Role
from app.features.users.model import User
from app.features.statuses.model import Status
from app.features.orders.model import Order

_MODELS = {
    Role.__tablename__: Role,
    User.__tablename__: User,
    Status.__tablename__: Status,
    Order.__tablename__: Order,
}


class ForeignKeyViolationError(Exception):
    pass


class UniqueViolationError(Exception):
    def __init__(self, column):
        self.column = column


def convert_integrity_error(dialect_name: str, err: IntegrityError) -> Exception:
    if dialect_name == 'postgresql':
        pg_code = getattr(err.orig, 'pgcode')

        if pg_code == '23503':
            return ForeignKeyViolationError()
        elif pg_code == '23505':
            err_text = str(err)

            table_name = err_text.split('INSERT INTO ')[1].split(' ')[0]
            column_name = err_text.split('Key (')[1].split(')')[0]

            return UniqueViolationError(inspect(_MODELS[table_name]).columns[column_name])

    return err
