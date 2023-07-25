from telebot.async_telebot import State
from telebot.asyncio_handler_backends import StatesGroup


class ExchangeStates(StatesGroup):
    exchange_type = State()
    fiat_src = State()
    fiat_dst = State()
    src_payment_types = State()
    dst_payment_types = State()
    src_amount = State()
    dst_amount = State()

