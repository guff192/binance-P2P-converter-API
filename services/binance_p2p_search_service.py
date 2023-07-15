from enum import Enum
import httpx

from pydantic import BaseModel, Field


API_URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


# API Request models
class TradeType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class P2PCryptoAssetType(str, Enum):
    USDT = 'USDT'
    BTC = 'BTC'
    BUSD = 'BUSD'
    BNB = 'BNB'
    ETH = 'ETH'


class AdvSearchRequestModel(BaseModel):
    fiat: str
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


class AdvSearchResponseModel(BaseModel):
    code: int
    message: str | None = None
    messageDetail: str | None = None
    data: list[AdvData] | None
    total: int
    success: bool


async def get_best_p2p_usdt_buy_course(
        fiat: str,
        pay_types: list[str] = [],
        amount: float = 0,
        ) -> AdvData: 
    req_model = AdvSearchRequestModel(
        fiat=fiat,
        page=1,
        rows=1,
        trade_type=TradeType.BUY,
        asset=P2PCryptoAssetType.USDT,
        pay_types=pay_types,
        trans_amount=amount,
    )

    adv_list = await _get_p2p_adv_list(req_model)
    return adv_list[0]


async def get_best_p2p_usdt_sell_course(
        fiat: str,
        pay_types: list[str] = [],
        amount: float = 0,
        ) -> AdvData: 
    req_model = AdvSearchRequestModel(
        fiat=fiat,
        page=1,
        rows=1,
        trade_type=TradeType.SELL,
        asset=P2PCryptoAssetType.USDT,
        pay_types=pay_types,
        trans_amount=amount
    )

    adv_list = await _get_p2p_adv_list(req_model)
    return adv_list[0]


async def _get_p2p_adv_list(request_data: AdvSearchRequestModel) -> list[AdvData]:
    # getting response
    response: httpx.Response = await _get_binance_adv_search_response(request_data)

    # parsing response
    try:
        adv_data_list = _parse_adv_data(response)
    except ApiEmptyResponseError as e:
        print('API returned empty response:', e)
        return []
    else:
        return adv_data_list


async def _get_binance_adv_search_response(request_data: AdvSearchRequestModel) -> httpx.Response:
    # TODO: catch possible errors
    async with httpx.AsyncClient(base_url=API_URL) as client:
        request_object = request_data.model_dump(by_alias=True)
        response: httpx.Response = await client.post('/', json=request_object)
        return response


class ApiResponseError(Exception): 
    """Can't get data from search API"""


class ApiEmptyResponseError(Exception):
    "API returned empty data in response"


def _parse_adv_data(api_response: httpx.Response) -> list[AdvData]:
    response_object = AdvSearchResponseModel(**api_response.json())
    if response_object.code != 0:
        raise ApiResponseError

    useful_data = response_object.data
    if useful_data is None:
        raise ApiEmptyResponseError

    return useful_data

