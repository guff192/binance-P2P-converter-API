from asyncio import create_task

from models.binance_models import FiatConvertOperation
from .binance_adv_search_service import (
        get_best_p2p_usdt_buy_course,
        get_best_p2p_usdt_sell_course
        )


class BothAmountsError(Exception):
    """Both source and destination amounts provided"""


async def get_best_fiat_change_operation(
        fiat_src: str,
        fiat_dst: str,
        src_payment_type: str,
        dst_payment_type: str,
        src_amount: float = 0,
        dst_amount: float = 0,
        ) -> FiatConvertOperation:
    if src_amount != 0 and dst_amount != 0:
        raise BothAmountsError('Provide either {fiat_src} or {fiat_dst} amount!')

    fiat_src_task = create_task(get_best_p2p_usdt_buy_course(
        fiat=fiat_src,
        amount=src_amount,
        pay_types=[src_payment_type]
    ))
    fiat_dst_task = create_task(get_best_p2p_usdt_sell_course(
        fiat=fiat_dst,
        amount=dst_amount,
        pay_types=[dst_payment_type]
    ))

    best_src_p2p_operation = await fiat_src_task
    best_dst_p2p_operation = await fiat_dst_task

    if src_amount != 0:
        dst_amount = src_amount / best_src_p2p_operation.course * best_dst_p2p_operation.course
        best_dst_p2p_operation = await get_best_p2p_usdt_sell_course(
                fiat=fiat_dst,
                amount=dst_amount,
                pay_types=[dst_payment_type]
                )
    elif dst_amount != 0:
        src_amount = dst_amount / best_dst_p2p_operation.course * best_src_p2p_operation.course
        best_src_p2p_operation = await get_best_p2p_usdt_buy_course(
                fiat=fiat_dst,
                amount=dst_amount,
                pay_types=[src_payment_type]
                )
        
    course = best_dst_p2p_operation.course / best_src_p2p_operation.course
    operation = FiatConvertOperation(
            course=course,
            src_amount=src_amount,
            fiat_src_operation=best_src_p2p_operation,
            fiat_dst_operation=best_dst_p2p_operation
            )

    return operation


async def main():
    operation = await get_best_fiat_change_operation(
            'RUB',
            'AMD',
            src_payment_type="TinkoffNew",
            dst_payment_type="Ardshinbank",
            src_amount=3000,
            )

    print(f'{operation.course = }\ninverted_course = {1/operation.course}')
    print('\n'*2)

    print(f'RUB: {operation.fiat_src_operation.course}, {operation.fiat_src_operation.advertiser_url}\n')
    print(f'RUB: {operation.fiat_dst_operation.course}, {operation.fiat_dst_operation.advertiser_url}\n')


if __name__ == '__main__':
    from asyncio import run
    run(main())

