from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
