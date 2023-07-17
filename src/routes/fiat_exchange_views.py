from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from enums.binance_enums import P2PCryptoAssetType, P2PFiatCurrencyType, TradeType
from models.binance_models import FiatConvertOperation, P2PExchangeOperation
from services.binance import (
    get_best_p2p_usdt_buy_course,
    get_best_p2p_usdt_sell_course,
)
from services.binance.binance_fiat_exchange_service import get_best_fiat_change_operation


fiat_exchange_router = APIRouter(prefix='/fiat-exchange')


class GetFiatCryptoCourseSchema(BaseModel):
    fiat: P2PFiatCurrencyType
    banks: list[str]
    fiat_amount: float = 0
    crypto: P2PCryptoAssetType = P2PCryptoAssetType.USDT
    operation_type: TradeType 


@fiat_exchange_router.post('/to_crypto')
async def get_fiat_crypto_courses(
    request: GetFiatCryptoCourseSchema,
) -> P2PExchangeOperation:
    """"""
    if request.crypto != P2PCryptoAssetType.USDT:
        raise NotImplementedError

    match request.operation_type:
        case TradeType.BUY:
            operation = await get_best_p2p_usdt_buy_course(
                fiat=request.fiat,
                pay_types=request.banks,
                amount=request.fiat_amount
            )
        case TradeType.SELL:
            operation = await get_best_p2p_usdt_sell_course(
                fiat=request.fiat,
                pay_types=request.banks,
                amount=request.fiat_amount
            )

    return operation


class GetFiatFiatCourseSchema(BaseModel):
    fiat_src: P2PFiatCurrencyType
    fiat_dst: P2PFiatCurrencyType
    banks_src: list[str]
    banks_dst: list[str]
    fiat_src_amount: float = 0
    fiat_dst_amount: float = 0


@fiat_exchange_router.post('/to_fiat')
async def get_fiat_fiat_courses(
    request: GetFiatFiatCourseSchema,
) -> FiatConvertOperation:
    """"""
    operation = await get_best_fiat_change_operation(
        fiat_src=request.fiat_src,
        fiat_dst=request.fiat_dst,
        src_payment_types=request.banks_src,
        dst_payment_types=request.banks_dst,
        src_amount=request.fiat_src_amount,
        dst_amount=request.fiat_dst_amount,
    )

    return operation

