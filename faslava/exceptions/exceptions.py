from faslava.core.utils import gettext_lazy as _


class BaseException(Exception):
    def __init__(self, http_error_code: int = 500, *args):
        self.http_error_code = http_error_code
        return super().__init__(*args)


class EngineNotCreatedException(BaseException):
    def __init__(self, *args):
        if "message" not in args:
            self.message = _("Engine is not created.")
        return super().__init__(*args)


class InvalidPaginationOffset(BaseException):
    def __init__(self, *args):
        if "message" not in args:
            self.message = _("Page not found")
        return super().__init__(http_error_code=404, *args)
