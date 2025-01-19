from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from faslava.logging.logging_manager import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.critical(
                f"AN UNKNOWN EXCEPTION WAS ENCOUNTERED IN THE APPLICATION: {e}"
            )
            raise e
