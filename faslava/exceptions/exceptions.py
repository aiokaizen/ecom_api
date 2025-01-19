from typing import Optional
from faslava.core.messages import UNKNOWN_ERROR_MESSAGE
from faslava.core.utils import gettext_lazy as _


class BaseException(Exception):
    def __init__(
        self, *, http_error_code: int = 500, message: Optional[str] = None, **kwargs
    ):
        self.http_error_code: int = http_error_code
        self.message: str = message or UNKNOWN_ERROR_MESSAGE
        return super().__init__(**kwargs)


class EngineNotCreatedException(BaseException):
    def __init__(self, *, message: Optional[str] = None, **kwargs):
        if not message:
            message = _("Engine not created.")
        return super().__init__(message=message, **kwargs)


class InvalidPaginationOffset(BaseException):
    def __init__(self, *, message: Optional[str] = None, **kwargs):
        if not message:
            message = _("Page not found")
        return super().__init__(http_error_code=404, message=message, **kwargs)
