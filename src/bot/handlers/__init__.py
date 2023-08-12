from telebot.async_telebot import AsyncTeleBot

from .main_menu_handlers import register_main_menu_handlers
from .start_help_handlers import register_start_help_handlers


def register_handlers(bot: AsyncTeleBot):
    register_start_help_handlers(bot)
    register_main_menu_handlers(bot)

