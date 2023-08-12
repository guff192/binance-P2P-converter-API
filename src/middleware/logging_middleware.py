from typing import Callable
from fastapi import Body, Request, Response
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response: Response = await call_next(request)

        request_method = request.method
        request_path = request.url.path
        request_query_params = dict(request.query_params)

        response.background = BackgroundTask(
            logger.debug,
            f'''
HTTP Request:
{request_method} {request_path} | {request_query_params=}
'''
        )

        return response

