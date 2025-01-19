from fastapi import HTTPException, Request
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse


class BaseMiddleware:
    """Custom base middleware to avoid some problems with scarlette's own BaseHTTPMiddleware."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Call this line in your code in case you want to interact with the request.
        # request = Request(scope, receive=receive)
        await self.app(scope, receive, send)

    async def _send_error_response(
        self, exc: HTTPException, receive: Receive, scope: Scope, send: Send
    ):
        """Returns a HTTPException instance as a JSON response."""
        response = JSONResponse(
            content={"detail": exc.detail}, status_code=exc.status_code
        )
        await response(scope, receive=receive, send=send)
