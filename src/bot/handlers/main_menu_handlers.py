from loguru import logger
from telebot.async_telebot import State
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot.states.exchange_states import ExchangeStates
from bot.filters.main_menu_filters import (
    operation_type_factory,
    fiat_src_factory,
    fiat_dst_factory,
    src_payment_types_factory,
    dst_payment_types_factory,
)
from bot.keyboards.main_menu import (
    get_fiat_src_keyboard,
    get_fiat_dst_keyboard,
    get_src_payment_types_keyboard,
    get_dst_payment_types_keyboard,
)

from services import binance as binance_service


def register_main_menu_handlers(bot: AsyncTeleBot):
    bot.register_callback_query_handler(
       callback=handle_operation_type_select,
       func=operation_type_factory.filter().check,
       pass_bot=True,
    )

    bot.register_callback_query_handler(
       callback=handle_fiat_dst_select,
       func=fiat_dst_factory.filter().check,
       pass_bot=True,
    )
    bot.register_callback_query_handler(
       callback=handle_fiat_src_select,
       func=fiat_src_factory.filter().check,
       pass_bot=True,
    )

    bot.register_callback_query_handler(
       callback=handle_src_payment_type,
       func=src_payment_types_factory.filter().check,
       pass_bot=True,
    )
    bot.register_callback_query_handler(
       callback=handle_dst_payment_type,
       func=dst_payment_types_factory.filter().check,
       pass_bot=True,
    )

    bot.register_message_handler(
        callback=handle_src_amount,
        func=lambda message: message.text.isdigit(),
        pass_bot=True
    )


async def _set_state_with_new_text_and_keyboard(
    bot: AsyncTeleBot,
    user_id: int,
    chat_id: int,
    message_id: int,
    state: State,
    text: str,
    keyboard: InlineKeyboardMarkup | None
) -> None:
    logger.info(f'changing state to {state.name}\n\n')

    await bot.set_state(user_id, state, chat_id)

    await bot.edit_message_text(
        text,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=keyboard
    )


async def _set_state_and_send_message_with_keyboard(bot: AsyncTeleBot,
    user_id: int,
    chat_id: int,
    state: State,
    text: str,
    keyboard: InlineKeyboardMarkup | None
) -> None:
    logger.info(f'changing state to {state.name}\n\n')

    await bot.set_state(user_id, state, chat_id)
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
    )



async def handle_operation_type_select(call: CallbackQuery, bot: AsyncTeleBot): 
    callback_data = operation_type_factory.parse(callback_data=call.data)
    logger.debug(callback_data)

    state = await bot.get_state(call.from_user.id, call.message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(call.from_user.id, call.message.chat.id,
       operation_type=callback_data['operation']
    )
    async with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        logger.debug(data)

    await _set_state_with_new_text_and_keyboard(
        bot,
        call.from_user.id,
        call.message.chat.id,
        call.message.id,
        ExchangeStates.fiat_src,
        'Пожалуйста, выбери фиатную валюту ИЗ которой будем переводить:',
        get_fiat_src_keyboard()
    )

    logger.debug(await bot.get_state(call.from_user.id, call.message.chat.id))


async def handle_fiat_src_select(call: CallbackQuery, bot: AsyncTeleBot):
    logger.info('received CallbackQuery for fiat_src')
    callback_data = fiat_src_factory.parse(callback_data=call.data)
    logger.debug(callback_data)
    
    state = await bot.get_state(call.from_user.id, call.message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(call.from_user.id, call.message.chat.id,
       fiat_src=callback_data['fiat']
    )
    async with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        logger.debug(data)

        if data['operation_type'] == 'fiat':
            await _set_state_with_new_text_and_keyboard(
                bot,
                call.from_user.id,
                call.message.chat.id,
                call.message.id,
                ExchangeStates.fiat_dst,
                'Пожалуйста, выбери фиатную валюту В которую будем переводить:',
                get_fiat_dst_keyboard()
            )
        elif data['operation_type'] == 'crypto':
            await _set_state_with_new_text_and_keyboard(
                bot,
                call.from_user.id,
                call.message.chat.id,
                call.message.id,
                ExchangeStates.src_payment_types,
                f'Пожалуйста, выбери способ перевода в {data["fiat_src"]}:',
                get_src_payment_types_keyboard(fiat_src=data['fiat_src'])
            )


async def handle_fiat_dst_select(call: CallbackQuery, bot: AsyncTeleBot):
    logger.info('received CallbackQuery for fiat_dst')
    callback_data = fiat_dst_factory.parse(callback_data=call.data)
    logger.debug(callback_data)
    
    state = await bot.get_state(call.from_user.id, call.message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(call.from_user.id, call.message.chat.id,
       fiat_dst=callback_data['fiat']
    )
    async with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        logger.debug(data)

        await _set_state_with_new_text_and_keyboard(
            bot,
            call.from_user.id,
            call.message.chat.id,
            call.message.id,
            ExchangeStates.src_payment_types,
            f'Пожалуйста, выбери способ перевода в {data["fiat_src"]}:',
            get_src_payment_types_keyboard(fiat_src=data['fiat_src'])
        )


async def handle_src_payment_type(call: CallbackQuery, bot: AsyncTeleBot):
    logger.info('received CallbackQuery for src_payment_type')
    callback_data = src_payment_types_factory.parse(callback_data=call.data)
    logger.debug(callback_data)
    
    state = await bot.get_state(call.from_user.id, call.message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(call.from_user.id, call.message.chat.id,
       src_payment_type=callback_data['payment_type']
    )
    async with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        logger.debug(data)

        if data['operation_type'] == 'crypto':
            await _set_state_with_new_text_and_keyboard(
                bot,
                call.from_user.id,
                call.message.chat.id,
                call.message.id,
                ExchangeStates.src_amount,
                f'Пожалуйста, введи сумму (только число, 0 — не указывать сумму) в {data["fiat_src"]}.:',
                None
            )
        elif data['operation_type'] == 'fiat':
            await _set_state_with_new_text_and_keyboard(
                bot,
                call.from_user.id,
                call.message.chat.id,
                call.message.id,
                ExchangeStates.dst_payment_types,
                f'Пожалуйста, выбери способ перевода в {data["fiat_dst"]}:',
                get_dst_payment_types_keyboard(fiat_dst=data['fiat_dst'])
            )


async def handle_dst_payment_type(call: CallbackQuery, bot: AsyncTeleBot):
    logger.info('received CallbackQuery for dst_payment_type')
    callback_data = dst_payment_types_factory.parse(callback_data=call.data)
    logger.debug(callback_data)
    
    state = await bot.get_state(call.from_user.id, call.message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(call.from_user.id, call.message.chat.id,
       dst_payment_type=callback_data['payment_type']
    )
    async with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        logger.debug(data)

        await _set_state_and_send_message_with_keyboard(
            bot,
            call.from_user.id,
            call.message.chat.id,
            ExchangeStates.src_amount,
            f'Пожалуйста, введи сумму (только число, 0 — не указывать сумму) в {data["fiat_src"]}:',
            None
        )


async def handle_src_amount(message: Message, bot: AsyncTeleBot):
    logger.info('received CallbackQuery for src_amount')
    src_amount = float(message.text) if message.text else 0.

    state = await bot.get_state(message.from_user.id, message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(message.from_user.id, message.chat.id,
       src_amount=src_amount
    )
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.debug(data)

        if data['operation_type'] == 'crypto':
            fiat_src=data['fiat_src']
            src_payment_types=[data['src_payment_type']]
            src_amount=data['src_amount']
            operation = await binance_service.get_best_p2p_usdt_buy_course(
                fiat=fiat_src,
                pay_types=src_payment_types,
                amount=src_amount,
            )
            await bot.send_message(
                chat_id=message.chat.id,
                text=str(operation.model_dump())
            )

        elif data['operation_type'] == 'fiat':
            if not src_amount:
                await _set_state_and_send_message_with_keyboard(
                    bot,
                    message.from_user.id,
                    message.chat.id,
                    ExchangeStates.dst_amount,
                    f'Пожалуйста, введи сумму (только число, 0 — не указывать сумму) в {data["fiat_dst"]}:',
                    None
                )
            else:
                fiat_src=data['fiat_src']
                fiat_dst=data['fiat_dst']
                src_payment_types=[data['src_payment_type']]
                dst_payment_types=[data['dst_payment_type']]
                src_amount=data['src_amount']
                dst_amount=0
                operation = await binance_service.get_best_fiat_change_operation(
                    fiat_src=fiat_src,
                    fiat_dst=fiat_dst,
                    src_payment_types=src_payment_types,
                    dst_payment_types=dst_payment_types,
                    src_amount=src_amount,
                    dst_amount=dst_amount,
                )

                formatted_operation = f'Перевод из {fiat_src} в {fiat_dst}:\n'
                formatted_operation += f'Курс:\n'
                formatted_operation += f'1 {fiat_src} = {operation.course} {fiat_dst}\n'
                formatted_operation += f'1 {fiat_dst} = {operation.inverted_course} {fiat_src}\n'
                formatted_operation += f'\nЛимиты обмена {fiat_src}:'
                formatted_operation += f'{operation.fiat_src_operation.min_amount} — {operation.fiat_src_operation.min_amount}'
                formatted_operation += f'\nЛимиты обмена {fiat_dst}:'
                formatted_operation += f'{operation.fiat_dst_operation.min_amount} — {operation.fiat_dst_operation.min_amount}'
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=formatted_operation
                )



async def handle_dst_amount(message: Message, bot: AsyncTeleBot):
    logger.info('received CallbackQuery for dst_amount')
    dst_amount = float(message.text) if message.text else 0.

    state = await bot.get_state(message.from_user.id, message.chat.id)
    logger.debug(f'{state = }')

    await bot.add_data(message.from_user.id, message.chat.id,
       dst_amount=dst_amount
    )
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.debug(data)

        fiat_src=data['fiat_src']
        fiat_dst=data['fiat_dst']
        src_payment_types=[data['src_payment_type']]
        dst_payment_types=[data['dst_payment_type']]
        src_amount=data['src_amount']
        dst_amount=data['dst_amount']
        operation = await binance_service.get_best_fiat_change_operation(
            fiat_src=fiat_src,
            fiat_dst=fiat_dst,
            src_payment_types=src_payment_types,
            dst_payment_types=dst_payment_types,
            src_amount=src_amount,
            dst_amount=dst_amount,
        )

        formatted_operation = f'перевод из {fiat_src} в {fiat_dst}:\n'
        formatted_operation += f'курс:\n'
        formatted_operation += f'1 {fiat_src} = {operation.course} {fiat_dst}\n'
        formatted_operation += f'1 {fiat_dst} = {operation.inverted_course} {fiat_src}\n'
        formatted_operation += f'\nлимиты обмена {fiat_src}:'
        formatted_operation += f'{operation.fiat_src_operation.min_amount} — {operation.fiat_src_operation.min_amount}'
        formatted_operation += f'\nлимиты обмена {fiat_dst}:'
        formatted_operation += f'{operation.fiat_dst_operation.min_amount} — {operation.fiat_dst_operation.min_amount}'
        await bot.send_message(
            chat_id=message.chat.id,
            text=formatted_operation
        )

