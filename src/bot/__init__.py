# coding: utf-8
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from bot.handlers import register_handlers


# TODO: read this from env
BOT_TOKEN = '5583301917:AAFditP-f1uBgdkyLxnC4JZUco0ZX37KgE8'
ADMIN_ID = '218710119'

state_storage = StateMemoryStorage()
bot = AsyncTeleBot(BOT_TOKEN, state_storage=state_storage)

async def configure_bot():
    register_handlers(bot)

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await bot.set_webhook(
        url='https://40f0-185-115-6-3.ngrok-free.app/api/v1/telegram/webhook',
        drop_pending_updates=True,
    )

    webhook_info = await bot.get_webhook_info()
    admin_info_message = f'bot is configured and running on webhook:\n\n{webhook_info}'
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_info_message
    )

