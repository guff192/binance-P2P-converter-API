from pydantic import BaseModel


class P2PExchangeOperation(BaseModel):
    fiat: str
    crypto: str
    course: float
    operation_type: str
    fiat_amount: float
    advertiser_url: str


class FiatConvertOperation(BaseModel):
    course: float
    src_amount: float
    fiat_src_operation: P2PExchangeOperation
    fiat_dst_operation: P2PExchangeOperation


