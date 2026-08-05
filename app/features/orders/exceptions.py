from app.core.base.exception import BaseError


class NonExistentOrderError(BaseError):
    status_code = 404
    detail = 'The specified order does not exist'


class SameStatusError(BaseError):
    status_code = 400
    detail = 'Current status and new status are the same'


class SameExecutorError(BaseError):
    status_code = 400
    detail = 'Current executor and new executor are the same'
