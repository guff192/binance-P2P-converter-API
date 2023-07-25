from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('Fiat ↔️ Crypto', callback_data='crypto'),
        InlineKeyboardButton('Fiat ↔️ Fiat', callback_data='fiat')
    )

    return markup

