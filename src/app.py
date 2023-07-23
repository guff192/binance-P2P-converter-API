# coding: utf-8
from logger import logger
from fastapi import FastAPI
import uvicorn

from routes import root_api_router
from middleware import register_middlewares


app = FastAPI()
app.include_router(root_api_router)
register_middlewares(app)


@app.on_event('startup')
def on_startup():
    logger.info('starting the app.....')


def run():
    uvicorn.run(
        app=__name__+':app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )


if __name__ == '__main__':
    run()

