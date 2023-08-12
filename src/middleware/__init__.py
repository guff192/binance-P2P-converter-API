from fastapi import FastAPI

from .logging_middleware import RequestLoggingMiddleware


def register_all_middleware(app: FastAPI):
    app.add_middleware(RequestLoggingMiddleware)

