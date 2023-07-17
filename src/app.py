# coding: utf-8
from fastapi import FastAPI
import uvicorn

from routes import root_api_router


app = FastAPI()
app.include_router(root_api_router)


def run():
    uvicorn.run(
        app=__name__+':app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )


if __name__ == '__main__':
    run()

