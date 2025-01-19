import traceback

from starlette.types import Receive, Scope, Send

from fastapi import HTTPException

from faslava.config.configuration import settings
from faslava.core.messages import UNKNOWN_ERROR_MESSAGE
from faslava.core.utils import gettext_lazy as _
from faslava.exceptions.exceptions import BaseException
from faslava.enums.enums import APIResponseStatusEnum
from faslava.middlewares.base_middleware import BaseMiddleware
from faslava.serializers.api_serializers import APIResponse


class ExceptionsMiddleware(BaseMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        try:
            return await super().__call__(scope, receive, send)
        except BaseException as e:
            response = HTTPException(
                status_code=e.http_error_code,
                detail=APIResponse(
                    status=APIResponseStatusEnum.ERROR, message=e.message
                ).model_dump(),
            )
            await self._send_error_response(response, receive, scope, send)
        except Exception:
            if settings.DEBUG:
                traceback.print_exc()
            response = HTTPException(
                status_code=500,
                detail=APIResponse(
                    status=APIResponseStatusEnum.ERROR,
                    message=UNKNOWN_ERROR_MESSAGE,
                ).model_dump(),
            )
            await self._send_error_response(response, receive, scope, send)
