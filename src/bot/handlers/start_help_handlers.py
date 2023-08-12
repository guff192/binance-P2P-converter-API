from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from loguru import logger

from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.states.exchange_states import ExchangeStates


def register_start_help_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(handle_start, commands=['start', 'help'], pass_bot=True)


# /start and /help commands handler
async def handle_start(message: Message, bot: AsyncTeleBot):
    logger.info('received /start or /help command')
    # Отправляем приветственное сообщение и информацию о боте
    await bot.send_message(message.chat.id, 'Привет! Я бот, который поможет тебе узнать актуальные курсы для покупки крипты с помощью Binance P2P, а также связки для обмена фиатной валюты Фиат1 ↔️ Крипта ↔️ Фиат2.')
    await bot.set_state(
        message.from_user.id,
        ExchangeStates.exchange_type,
        message.chat.id
    )
    await bot.send_message(
        message.chat.id,
        'Сначала выбери тип обмена, который тебя интересует:',
        reply_markup=get_main_menu_keyboard()
    )
