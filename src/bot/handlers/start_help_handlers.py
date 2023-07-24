from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from loguru import logger


def register_start_help_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(handle_start, commands=['start', 'help'], pass_bot=True)


# /start and /help commands handler
async def handle_start(message: Message, bot: AsyncTeleBot):
    logger.info('received /start or /help command')
    # Отправляем приветственное сообщение и информацию о боте
    await bot.send_message(message.chat.id, 'Привет! Я бот, который поможет тебе узнать актуальные курсы для покупки крипты с помощью Binance P2P, а также связки для обмена фиатной валюты Фиат1 ➡️ Крипта ➡️ Фиат2.')
    await bot.send_message(message.chat.id, 'Могу чем-то помочь?')
