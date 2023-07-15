# coding: utf-8
import asyncio

from services.binance import get_best_fiat_change_operation


async def main():
    operation = await get_best_fiat_change_operation(
            'RUB',
            'AMD',
            src_payment_type="TinkoffNew",
            dst_payment_type="Ardshinbank",
            src_amount=3000,
    )
    
    for key, value in operation.model_dump().items():
        if not isinstance(value, dict):
            print(f'{key}: {value}')
        else:
            print(key+': {')
            for k, v in value.items():
                print(f'    {k}: {v}')
            print('}')


asyncio.run(main())

