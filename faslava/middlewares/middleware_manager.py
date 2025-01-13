from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from faslava.config.configuration import settings
from faslava.middlewares.logging_middleware import LoggingMiddleware


def inject_middlewares(app: FastAPI):
    allowed_hosts = settings.serialize_allowed_hosts()
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
    app.add_middleware(LoggingMiddleware)
