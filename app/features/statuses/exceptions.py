from app.core.base.exception import BaseError


class NonExistentStatusError(BaseError):
    status_code = 404
    detail = 'The specified status does not exist'
