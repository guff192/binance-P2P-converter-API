from fastapi import APIRouter, BackgroundTasks
from loguru import logger
from telebot.types import Update

from bot import bot
from models.telegram_models import TelegramWebhookRequest


telegram_router = APIRouter(prefix='/telegram')


@telegram_router.post("/webhook")
async def process_webhook(
    request: dict,
    background_tasks: BackgroundTasks
) -> None:
    """
    Process webhook calls
    """
    if request:
        update = Update.de_json(request)
        if isinstance(update, Update):
            logger.info('received telegram webhook wtih Update')
            background_tasks.add_task(bot.process_new_updates, [update])
        return
    else:
        return
