from pydantic import BaseModel, computed_field

from enums.binance_enums import P2PCryptoAssetType, P2PFiatCurrencyType, TradeType


class P2PExchangeOperation(BaseModel):
    fiat: P2PFiatCurrencyType
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

    @computed_field
    @property
    def inverted_course(self) -> float:
        return 1/self.course


