from fastapi import APIRouter

from routes.fiat_exchange_views import fiat_exchange_router
from routes.telegram_views import telegram_router


root_api_router = APIRouter(prefix='/api/v1')
root_api_router.include_router(fiat_exchange_router)
root_api_router.include_router(telegram_router)

