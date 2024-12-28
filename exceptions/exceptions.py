from utils.utils import gettext_lazy as _


class BaseException(Exception):

    def __init__(self, *args):
        return super().__init__(*args)


class EngineNotCreatedException(BaseException):

    def __init__(self, *args):
        if "message" not in args:
            self.message = _("Engine is not created.")
        return super().__init__(*args)
