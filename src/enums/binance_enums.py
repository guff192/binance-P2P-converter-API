from enum import Enum


class TradeType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class P2PCryptoAssetType(str, Enum):
    USDT = 'USDT'
    BTC = 'BTC'
    BUSD = 'BUSD'
    BNB = 'BNB'
    ETH = 'ETH'


