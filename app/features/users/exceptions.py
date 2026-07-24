from app.core.base.exception import BaseError


class SameUsernameError(BaseError):
    status_code = 400
    detail = 'The new username and the current one are the same'


class TakenUsernameError(BaseError):
    status_code = 409
    detail = 'This username is already taken'


class SamePasswordError(BaseError):
    status_code = 400
    detail = 'The current password and the new password are the same'
