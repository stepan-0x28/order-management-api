class BaseError(Exception):
    status_code: int
    detail: str
