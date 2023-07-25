# coding: utf-8
from logger import logger
from fastapi import FastAPI
import uvicorn

from routes import root_api_router
from middleware import register_middlewares
from bot import bot


app = FastAPI()
app.include_router(root_api_router)
register_middlewares(app)


@app.on_event('startup')
async def on_startup():
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await bot.set_webhook(
        url='https://b7e4-37-252-94-246.ngrok-free.app/api/v1/telegram/webhook',
        drop_pending_updates=True,
    )
    logger.info('starting the app.....')


@app.on_event('shutdown')
async def on_shutdown():
    logger.info('shutting down the app...')

    await bot.delete_webhook(
        drop_pending_updates=True
    )
    await bot.close_session()


def run():
    uvicorn.run(
        app=__name__+':app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )


if __name__ == '__main__':
    run()

