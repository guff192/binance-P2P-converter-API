from fastapi import HTTPException

from enums.binance_enums import P2PFiatCurrencyType


class BinanceApiResponseError(HTTPException): 
    """Can't get data from search API"""
    def __init__(self, *, err_message: str):
        self.status_code = 500
        self.detail = f'Error getting data from Binance API: {err_message}'
        self.headers = None


class BinanceApiEmptyResponseError(BinanceApiResponseError):
    "API returned empty data in response"
    def __init__(self, *, fiat: P2PFiatCurrencyType):
        super().__init__(
            err_message=f'API returned no data in response for {fiat.value}'
        )

