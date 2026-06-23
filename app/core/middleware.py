"""
ASGI Middleware for Request Correlation Tracking and Logging context.
"""
import uuid
import contextvars
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Context variable to hold the correlation ID for the duration of a request
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="system")

def get_correlation_id() -> str:
    """Returns the current request correlation ID."""
    return correlation_id_ctx.get()

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that reads/creates X-Correlation-ID and registers it
    into thread/async-local contextvars for structured logging.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        # Fetch existing header, or generate new UUID
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        # Token token to reset context after request
        token = correlation_id_ctx.set(correlation_id)
        
        try:
            response: Response = await call_next(request)
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        finally:
            correlation_id_ctx.reset(token)
