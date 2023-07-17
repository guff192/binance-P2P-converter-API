from asyncio import create_task

from fastapi import HTTPException
from enums.binance_enums import P2PFiatCurrencyType

from models.binance_models import FiatConvertOperation
from .binance_adv_search_service import (
        get_best_p2p_usdt_buy_course,
        get_best_p2p_usdt_sell_course
        )


class BothAmountsError(HTTPException):
    """Both source and destination amounts provided"""
    def __init__(self):
        self.status_code = 400
        self.detail = 'You may set either src_amount or dst_amount, not both of them!'
        self.headers = None


async def get_best_fiat_change_operation(
        fiat_src: P2PFiatCurrencyType,
        fiat_dst: P2PFiatCurrencyType,
        src_payment_types: list[str],
        dst_payment_types: list[str],
        src_amount: float = 0,
        dst_amount: float = 0,
        ) -> FiatConvertOperation:
    if src_amount != 0 and dst_amount != 0:
        raise BothAmountsError()

    fiat_src_task = create_task(get_best_p2p_usdt_buy_course(
        fiat=fiat_src,
        amount=src_amount,
        pay_types=src_payment_types
    ))
    fiat_dst_task = create_task(get_best_p2p_usdt_sell_course(
        fiat=fiat_dst,
        amount=dst_amount,
        pay_types=dst_payment_types
    ))

    best_src_p2p_operation = await fiat_src_task
    best_dst_p2p_operation = await fiat_dst_task

    if src_amount != 0:
        dst_amount = src_amount / best_src_p2p_operation.course * best_dst_p2p_operation.course
        best_dst_p2p_operation = await get_best_p2p_usdt_sell_course(
                fiat=fiat_dst,
                amount=dst_amount,
                pay_types=dst_payment_types
                )
    elif dst_amount != 0:
        src_amount = dst_amount / best_dst_p2p_operation.course * best_src_p2p_operation.course
        best_src_p2p_operation = await get_best_p2p_usdt_buy_course(
                fiat=fiat_dst,
                amount=dst_amount,
                pay_types=src_payment_types
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
            P2PFiatCurrencyType.RUB,
            P2PFiatCurrencyType.AMD,
            src_payment_types=["TinkoffNew"],
            dst_payment_types=["Ardshinbank", "ArCA"],
            src_amount=3000,
            )

    print(f'{operation.course = }\ninverted_course = {1/operation.course}')
    print('\n'*2)

    print(f'RUB: {operation.fiat_src_operation.course}, {operation.fiat_src_operation.advertiser_url}\n')
    print(f'RUB: {operation.fiat_dst_operation.course}, {operation.fiat_dst_operation.advertiser_url}\n')


if __name__ == '__main__':
    from asyncio import run
    run(main())

