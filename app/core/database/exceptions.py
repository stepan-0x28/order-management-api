from sqlalchemy.exc import IntegrityError


class UniqueViolationError(Exception):
    pass


class ForeignKeyViolationError(Exception):
    pass


_POSTGRES_ERROR_CODE_TO_EXCEPTION_CLASS = {
    '23505': UniqueViolationError,
    '23503': ForeignKeyViolationError
}


def convert_integrity_error(dialect_name: str, err: IntegrityError) -> Exception:
    if dialect_name == 'postgresql':
        # noinspection SpellCheckingInspection
        exception_class = _POSTGRES_ERROR_CODE_TO_EXCEPTION_CLASS.get(getattr(err.orig, 'pgcode'))

        if exception_class:
            return exception_class()

    return err
