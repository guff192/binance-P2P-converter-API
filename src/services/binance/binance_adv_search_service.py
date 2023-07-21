from fastapi import HTTPException
import httpx
from pydantic import BaseModel, Field

from models.binance_models import P2PExchangeOperation
from enums.binance_enums import P2PFiatCurrencyType, TradeType, P2PCryptoAssetType


API_URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


# API Request models
class AdvSearchRequestSchema(BaseModel):
    fiat: P2PFiatCurrencyType
    page: int = 1
    rows: int = 20
    trade_type: TradeType = Field(serialization_alias='tradeType')
    asset: P2PCryptoAssetType = P2PCryptoAssetType.USDT
    countries: list = [] # some traders set their country incorrect
    # pro_merchant_ads: bool = Field(default=False, serialization_alias='proMerchantAds')
    # shield_merchant_ads: bool = Field(default=False, serialization_alias='shieldMerchantAds')
    # publisher_type: None = Field(default=None, serialization_alias='publisherType')
    pay_types: list = Field(default=[], serialization_alias='payTypes')
    trans_amount: float = Field(default=0, serialization_alias='transAmount')


# API Response models
class Adv(BaseModel):
    adv_no: str = Field(validation_alias='advNo')
    fiat_unit: str = Field(alias='fiatUnit')
    price: float
    min_single_trans_amount: float = Field(alias='minSingleTransAmount')
    max_single_trans_amount: float = Field(alias='maxSingleTransAmount')


class Advertiser(BaseModel):
    user_no: str = Field(alias='userNo')
    real_name: str | None = Field(alias='realName')
    nickname: str = Field(alias='nickName')


class AdvData(BaseModel):
    adv: Adv
    advertiser: Advertiser


class AdvSearchResponseSchema(BaseModel):
    code: int
    message: str | None = None
    messageDetail: dict | None = None
    data: list[AdvData] | None
    total: int = 0
    success: bool


async def get_best_p2p_usdt_buy_course(
        fiat: P2PFiatCurrencyType,
        pay_types: list[str] = [],
        amount: float = 0,
        ) -> P2PExchangeOperation: 
    req_model = AdvSearchRequestSchema(
        fiat=fiat,
        page=1,
        rows=1,
        trade_type=TradeType.BUY,
        asset=P2PCryptoAssetType.USDT,
        pay_types=pay_types,
        trans_amount=amount,
    )

    adv_list = await _get_p2p_adv_list(req_model)

    try:
        best_adv_data = adv_list[0]
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail={'message': f'no courses for {fiat}, try to change your search conditions'}
        )

    operation = P2PExchangeOperation(
            fiat=fiat,
            crypto=P2PCryptoAssetType.USDT,
            course=best_adv_data.adv.price,
            operation_type=TradeType.BUY,
            fiat_amount=amount,
            advertiser_url=_get_advertiser_url(best_adv_data)
            )
    return operation


async def get_best_p2p_usdt_sell_course(
        fiat: P2PFiatCurrencyType,
        pay_types: list[str] = [],
        amount: float = 0,
        ) -> P2PExchangeOperation: 
    req_model = AdvSearchRequestSchema(
        fiat=fiat,
        page=1,
        rows=1,
        trade_type=TradeType.SELL,
        asset=P2PCryptoAssetType.USDT,
        pay_types=pay_types,
        trans_amount=amount
    )

    adv_list = await _get_p2p_adv_list(req_model)
    try:
        best_adv_data = adv_list[0]
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail={'message': f'no courses for {str(fiat.value)}, try to change your search conditions'}
        )

    operation = P2PExchangeOperation(
            fiat=fiat,
            crypto=P2PCryptoAssetType.USDT,
            course=best_adv_data.adv.price,
            operation_type=TradeType.SELL,
            fiat_amount=amount,
            advertiser_url=_get_advertiser_url(best_adv_data)
            )
    return operation


def _get_advertiser_url(adv_info: AdvData):
    advertiser_no = adv_info.advertiser.user_no
    return f'https://p2p.binance.com/en/advertiserDetail?advertiserNo={advertiser_no}'


async def _get_p2p_adv_list(request_data: AdvSearchRequestSchema) -> list[AdvData]:
    # getting response
    response: httpx.Response = await _get_binance_adv_search_response(request_data)

    # parsing response
    try:
        adv_data_list = _parse_adv_data(response)
    except BinanceApiEmptyResponseError as e:
        return []
    else:
        return adv_data_list


async def _get_binance_adv_search_response(request_data: AdvSearchRequestSchema) -> httpx.Response:
    # TODO: catch possible errors
    try:
        async with httpx.AsyncClient(base_url=API_URL) as client:
            request_object = request_data.model_dump(by_alias=True)
            response: httpx.Response = await client.post('/', json=request_object)
    except:
        raise BinanceApiResponseError('error while getting response from API')

    return response


def _parse_adv_data(api_response: httpx.Response) -> list[AdvData]:
    response_object = AdvSearchResponseSchema(**api_response.json())
    # if response_object.code != 0:
    #     raise ApiResponseError()

    useful_data = response_object.data
    if useful_data is None:
        raise BinanceApiEmptyResponseError

    return useful_data

