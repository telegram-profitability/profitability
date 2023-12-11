from abc import ABC
from abc import abstractmethod
from datetime import date
from datetime import timedelta

import httpx

from src.configs import TINKOFF_API_KEY


class AbstractStockClient(ABC):
    _client = httpx.AsyncClient()

    @abstractmethod
    async def get_stock_info(self, coin: str, timestamp: date = None) -> dict | None:
        raise NotImplementedError()

    async def _post(self, route: str, json: dict = None) -> dict | None:
        response = await self._client.post(url=route, json=json)
        return response.json() if response.status_code == 200 else None


class TinkoffInvestClient(AbstractStockClient):
    def __init__(self) -> None:
        self._api_key = TINKOFF_API_KEY
        self._client.base_url = "https://invest-public-api.tinkoff.ru/rest"
        self._client.headers = {"Authorization": f"Bearer {self._api_key}"}

    async def get_stock_info(self, ticker: str, timestamp: date = None) -> dict | None:
        route = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/FindInstrument"
        json = {
            "query": ticker,
            "instrumentKind": "INSTRUMENT_TYPE_SHARE",
            "apiTradeAvailableFlag": "true",
        }
        response = await self._post(route=route, json=json)
        if response is None:
            return None

        instruments: list | None = response.get("instruments", None)
        if instruments is None or len(instruments) == 0:
            return None

        ticker_id = instruments[0].get("uid", None)
        ticker_name = instruments[0].get("name", None)

        if ticker_id is None or ticker_name is None:
            return None

        if timestamp is None:
            route = "/tinkoff.public.invest.api.contract.v1.MarketDataService/GetLastPrices"
            json = {"instrumentId": [ticker_id]}
            prices_target = "lastPrices"
            price_object_name = "price"
        else:
            route = "/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"
            from_date = f"{timestamp.strftime("%Y-%m-%d")}T00:00:00Z"
            to_timestamp = timestamp + timedelta(days=1)
            to_date = f"{to_timestamp.strftime("%Y-%m-%d")}T00:00:00Z"
            json = {
                "from": from_date,
                "to": to_date,
                "interval": "CANDLE_INTERVAL_DAY",
                "instrumentId": ticker_id,
            }
            prices_target = "candles"
            price_object_name = "close"

        response = await self._post(route=route, json=json)
        if response is None:
            return None
        prices: list = response.get(prices_target, [])
        if len(prices) == 0:
            return None
        price_object = prices[0].get(price_object_name, {})

        units = price_object.get("units", None)
        nano = price_object.get("nano", None)
        if units is None or nano is None:
            return None

        price = float(units) + float(nano) * 0.000000001

        return {
            "id": ticker_id,
            "name": ticker_name,
            "timestamp": date.today() if timestamp is None else timestamp,
            "price": price,
        }
