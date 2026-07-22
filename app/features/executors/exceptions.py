from app.core.base.exception import BaseError


class NonExistentExecutorError(BaseError):
    status_code = 404
    detail = 'The specified executor does not exist'
