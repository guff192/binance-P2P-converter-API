# coding: utf-8
import asyncio

from binance_p2p_search_service import(
        get_best_p2p_usdt_buy_course, 
        get_best_p2p_usdt_sell_course
        )


async def get_best_fiat_change_course(
        fiat_src: str,
        fiat_dst: str,
        src_payment_type: str,
        dst_payment_type: str,
        src_amount: float = 0,
        dst_amount: float = 0,
        ):
    fiat_src_task = asyncio.create_task(get_best_p2p_usdt_buy_course(
        fiat=fiat_src,
        amount=src_amount,
        pay_types=[src_payment_type]
    ))
    fiat_dst_task = asyncio.create_task(get_best_p2p_usdt_sell_course(
        fiat=fiat_dst,
        amount=dst_amount,
        pay_types=[dst_payment_type]
    ))

    best_src_p2p_adv = await fiat_src_task
    best_dst_p2p_adv = await fiat_dst_task

    course = best_dst_p2p_adv.adv.price / best_src_p2p_adv.adv.price
    return course, best_src_p2p_adv, best_dst_p2p_adv


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

    base_advertiser_url = 'https://p2p.binance.com/en/advertiserDetail?advertiserNo='
    rub_advertiser_url = base_advertiser_url + rub_adv.advertiser.user_no
    amd_advertiser_url = base_advertiser_url + amd_adv.advertiser.user_no
    print(f'RUB: {rub_adv.adv.price}, {rub_advertiser_url}\n')
    print(f'AMD: {amd_adv.adv.price}, {amd_advertiser_url}\n')


asyncio.run(main())

