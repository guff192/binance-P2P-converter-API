# coding: utf-8
import asyncio
import time
import httpx
import json
from enum import Enum
from pydantic import BaseModel


api_url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


class TradeType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class P2PCryptoAssetType(str, Enum):
    USDT = 'USDT'
    BTC = 'BTC'
    BUSD = 'BUSD'
    BNB = 'BNB'
    ETH = 'ETH'


class AdvRequestDataModel(BaseModel):
    fiat: str
    page: int = 1
    rows: int = 20
    tradeType: TradeType
    asset: P2PCryptoAssetType = P2PCryptoAssetType.USDT
    countries: list = [] # some traders set their country incorrect
    proMerchantAds: bool = False
    shieldMerchantAds: bool = False
    publisherType: None = None
    payTypes: list = []
    transAmount: int = 0


request_data = {
    'fiat':'AMD',
    'page':1,
    'rows':20,
    'tradeType':'SELL',
    'asset':'USDT',
    'countries':[],
    'proMerchantAds':False,
    'shieldMerchantAds':False,
    'publisherType':None,
    'payTypes':[],
    'transAmount':0,
}


async def get_best_fiat_change_course(fiat_src, fiat_dst):
    fiat_src_task = asyncio.create_task(get_top_10_fiat_p2p_courses(
        fiat=fiat_src,
        tradeType=TradeType.BUY,
        crypto=P2PCryptoAssetType.USDT
    ))
    fiat_dst_task = asyncio.create_task(get_top_10_fiat_p2p_courses(
        fiat=fiat_dst,
        tradeType=TradeType.SELL,
        crypto=P2PCryptoAssetType.USDT
    ))

    fiat_src_p2p_prices = await fiat_src_task
    fiat_dst_p2p_prices = await fiat_dst_task

    course = float(fiat_dst_p2p_prices[0][1]) / float(fiat_src_p2p_prices[0][1])
    return course


async def get_top_10_fiat_p2p_courses(fiat: str, tradeType: TradeType, crypto: P2PCryptoAssetType): 
    req_model = AdvRequestDataModel(
        fiat=fiat,
        page=1,
        rows=10,
        tradeType=tradeType,
        asset=crypto,
    )

    return await get_p2p_courses(req_model)


async def get_p2p_courses(request_data: AdvRequestDataModel):
    async with httpx.AsyncClient() as client:
        r = await client.post(api_url, json=request_data.model_dump())
    response_object = json.loads(r.text)
        
    useful_data = response_object.get('data')

    adv_list = [item.get('adv') for item in useful_data]
    # adv_list.sort(key=lambda adv: adv.get('price'))

    price_list = [(
            adv.get('advNo'),
            adv.get('price'),
            adv.get('minSingleTransAmount'),
            adv.get('maxSingleTransAmount'),
        ) for adv in adv_list]
    return price_list


async def main():
    rub_amd_course = await get_best_fiat_change_course('RUB', 'AMD')
    print(f'{rub_amd_course = }')

asyncio.run(main())

