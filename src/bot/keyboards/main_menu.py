from typing import NamedTuple
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from enums.binance_enums import P2PFiatCurrencyType
from bot.filters.main_menu_filters import (
    operation_type_factory,
    fiat_src_factory, 
    fiat_dst_factory,
    src_payment_types_factory,
    dst_payment_types_factory
)


def get_operation_type_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text='Fiat ↔️ Crypto',
            callback_data=operation_type_factory.new(operation='crypto')
        ),
        InlineKeyboardButton(
            text='Fiat ↔️ Fiat',
            callback_data=operation_type_factory.new(operation='fiat')
        )
    )

    return markup


def get_fiat_src_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(*[
        InlineKeyboardButton(
            text=fiat.value,
            callback_data=fiat_src_factory.new(fiat=fiat.value)
            )
        for fiat in sorted(P2PFiatCurrencyType, key=lambda currency: currency.value)
    ]
    )

    return markup


def get_fiat_dst_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(*[
        InlineKeyboardButton(
            text=fiat.value,
            callback_data=fiat_dst_factory.new(fiat=fiat.value)
            )
        for fiat in sorted(P2PFiatCurrencyType, key=lambda currency: currency.value)
    ])

    return markup


class PaymentType(NamedTuple):
    identificator: str
    name: str
    

# TODO: Parse this from binance API
AMD_PAYMENT_TYPES = [
    PaymentType('Ardshinbank', 'Ardshinbank'),
    PaymentType('ArCA', 'ArCA'),
]

RUB_PAYMENT_TYPES = [
    PaymentType('TinkoffNew', 'Tinkoff'),
    PaymentType('Qiwi', 'Qiwi'),
]

PAYMENT_TYPES = {
    'RUB': RUB_PAYMENT_TYPES,
    'AMD': AMD_PAYMENT_TYPES,
}


def get_src_payment_types_keyboard(fiat_src: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(*[
        InlineKeyboardButton(
            text=payment_type.name,
            callback_data=src_payment_types_factory.new(payment_type=payment_type.identificator)
            )
        for payment_type in sorted(PAYMENT_TYPES[fiat_src], key=lambda bank: bank.name)
    ]
    )

    return markup


def get_dst_payment_types_keyboard(fiat_dst: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(*[
        InlineKeyboardButton(
            text=payment_type.name,
            callback_data=dst_payment_types_factory.new(payment_type=payment_type.identificator)
            )
        for payment_type in sorted(PAYMENT_TYPES[fiat_dst], key=lambda bank: bank.name)
    ]
    )

    return markup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return get_operation_type_keyboard()

