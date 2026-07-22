from app.core.base.exception import BaseError


class NonExistentRoleError(BaseError):
    status_code = 404
    detail = 'The specified role does not exist'


class InappropriateRoleError(BaseError):
    status_code = 403
    detail = 'Inappropriate role'
