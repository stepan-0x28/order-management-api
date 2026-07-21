from app.core.base.exception import BaseError


class IncorrectPasswordError(BaseError):
    status_code = 401
    detail = 'The current password is incorrect'


class IncorrectUsernameOrPasswordError(BaseError):
    status_code = 401
    detail = 'Incorrect username or password'


class NonExistentUserOrTokenExpiredError(BaseError):
    status_code = 401
    detail = 'The user does not exist or the token has expired'
