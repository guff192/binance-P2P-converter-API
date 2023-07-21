from fastapi import HTTPException


class BinanceApiResponseError(HTTPException): 
    """Can't get data from search API"""
    def __init__(self, err_message):
        self.status_code = 500
        self.detail = f'Error getting data from Binance API: {err_message}'
        self.headers = None


class BinanceApiEmptyResponseError(BinanceApiResponseError):
    "API returned empty data in response"
    def __init__(self):
        super().__init__('API returned no data in response')

