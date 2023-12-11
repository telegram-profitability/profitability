from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

import httpx

from src.clients.models import StockCurrentInfo
from src.configs import TINKOFF_API_KEY
from utils.http_client import AbstractHttpClient


class AbstractStockClient(ABC):
    @abstractmethod
    async def get_stock_current_info(self, coin: str) -> StockCurrentInfo | None:
        raise NotImplementedError()


class TinkoffInvestClient(AbstractStockClient):
    def __init__(self, client: AbstractHttpClient) -> None:
        self._api_key = TINKOFF_API_KEY
        self._client = client

    async def get_stock_current_info(self, ticker: str) -> StockCurrentInfo | None:
        stock = await self._get_id_and_name_by_tiker(ticker)
        if stock is None:
            return None

        stock_id, stock_name = stock

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = await self._client.post(
            headers=headers,
            url="https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetLastPrices",
            json={"instrumentId": [stock_id]},
        )
        if response is None:
            return None

        prices: list | None = response.get("lastPrices", None)
        if prices is None:
            return None

        price_object = prices[0].get("price", {})
        units = price_object.get("units", None)
        nano = price_object.get("nano", None)

        if units is None or nano is None:
            return None

        price = units + nano * 0.000000001

        return StockCurrentInfo(
            ticker=ticker, name=stock_name, time=datetime.now(timezone.utc), price=price
        )

    async def _get_id_and_name_by_tiker(self, ticker: str) -> tuple[str, str] | None:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = await self._client.post(
            headers=headers,
            url="https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/FindInstrument",
            json={
                "query": ticker,
                "instrumentKind": "INSTRUMENT_TYPE_SHARE",
                "apiTradeAvailableFlag": "true",
            },
        )

        if response is None:
            return None

        instruments: list | None = response.get("instruments", None)
        if instruments is None or len(instruments) == 0:
            return None

        ticker_id = instruments[0].get("uid", None)
        name = instruments[0].get("name", None)

        if ticker_id is None or name is None:
            return None

        return ticker_id, name
