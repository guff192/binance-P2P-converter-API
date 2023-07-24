# coding: utf-8
from telebot.async_telebot import AsyncTeleBot

from bot.handlers import register_message_handlers


# TODO: read this from env
BOT_TOKEN = "5583301917:AAFditP-f1uBgdkyLxnC4JZUco0ZX37KgE8"

# Создаем объект бота
bot = AsyncTeleBot(BOT_TOKEN)

register_message_handlers(bot)

