from pydantic import BaseModel

from enums.binance_enums import P2PCryptoAssetType, TradeType


class P2PExchangeOperation(BaseModel):
    fiat: str
    crypto: P2PCryptoAssetType
    course: float
    operation_type: TradeType
    fiat_amount: float
    advertiser_url: str


class FiatConvertOperation(BaseModel):
    course: float
    src_amount: float
    fiat_src_operation: P2PExchangeOperation
    fiat_dst_operation: P2PExchangeOperation


