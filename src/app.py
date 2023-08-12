# coding: utf-8
from logger import logger
from fastapi import FastAPI
import uvicorn

from routes import root_api_router
from middleware import register_all_middleware
from bot import bot, configure_bot


app = FastAPI()
app.include_router(root_api_router)
register_all_middleware(app)


@app.on_event('startup')
async def on_startup():
    await configure_bot()
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

