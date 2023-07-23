from fastapi import FastAPI

from .logging_middleware import RequestLoggingMiddleware


def register_middlewares(app: FastAPI):
    app.add_middleware(RequestLoggingMiddleware)

