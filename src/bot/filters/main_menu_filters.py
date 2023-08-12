from telebot.callback_data import CallbackData


operation_type_factory = CallbackData('operation', prefix='operation_type')
fiat_src_factory = CallbackData('fiat', prefix='fiat_src')
fiat_dst_factory = CallbackData('fiat', prefix='fiat_dst')
src_payment_types_factory = CallbackData('payment_type', prefix='src_payment_type')
dst_payment_types_factory = CallbackData('payment_type', prefix='dst_payment_type')

