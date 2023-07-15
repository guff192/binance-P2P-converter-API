from asyncio import create_task

from pydantic import BaseModel

from services.binance_p2p_search_service import (
        AdvData,
        get_best_p2p_usdt_buy_course,
        get_best_p2p_usdt_sell_course
        )


class P2PExchangeOperation(BaseModel):
    fiat: str
    crypto: str
    operation_type: str
    fiat_amount: float
    advertiser_url: str


class FiatConvertation(BaseModel):
    course: float
    amount: float
    fiat_src_adv_data: AdvData
    fiat_dst_adv_data: AdvData


async def get_best_fiat_change_course(
        fiat_src: str,
        fiat_dst: str,
        src_payment_type: str,
        dst_payment_type: str,
        src_amount: float = 0,
        dst_amount: float = 0,
        ):
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

    best_src_p2p_adv = await fiat_src_task
    best_dst_p2p_adv = await fiat_dst_task
    course = best_dst_p2p_adv.adv.price / best_src_p2p_adv.adv.price

    return course, best_src_p2p_adv, best_dst_p2p_adv


def _get_advertiser_url(adv_info: AdvData):
    advertiser_no = adv_info.advertiser.user_no
    return f'https://p2p.binance.com/en/advertiserDetail?advertiserNo={advertiser_no}'


async def main():
    amd_rub_course, rub_adv, amd_adv = await get_best_fiat_change_course(
            'RUB',
            'AMD',
            src_payment_type="TinkoffNew",
            dst_payment_type="Ardshinbank",
            src_amount=3000,
            )

    print(f'{amd_rub_course = }\ninverted_course = {1/amd_rub_course}')
    print('\n'*2)

    rub_advertiser_url = _get_advertiser_url(rub_adv)
    amd_advertiser_url = _get_advertiser_url(rub_adv)
    print(f'RUB: {rub_adv.adv.price}, {rub_advertiser_url}\n')
    print(f'AMD: {amd_adv.adv.price}, {amd_advertiser_url}\n')


if __name__ == '__main__':
    from asyncio import run
    run(main())

