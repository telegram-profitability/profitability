from abc import ABC
from abc import abstractmethod
from datetime import date
from datetime import timedelta
import logging
from typing import Any

import httpx

from src.configs import TINKOFF_API_KEY


class AbstractStockClient(ABC):
    _client = httpx.AsyncClient()

    @abstractmethod
    async def get_stock_info(self, coin: str, timestamp: date | None = None) -> dict | None:
        raise NotImplementedError()

    async def _post(self, route: str, json: dict | None = None) -> dict | None:
        logging.info("Sending POST request to cryptocurrency API")
        response = await self._client.post(url=route, json=json)
        logging.info("Response received")
        if response.status_code == 200:
            logging.info("Response status code is 200, returning dictionary")
            return response.json()
        logging.info(f"Response status code is {response.status_code}, returning None")
        return None


class TinkoffInvestClient(AbstractStockClient):
    def __init__(self) -> None:
        self._api_key = TINKOFF_API_KEY
        self._client.base_url = "https://invest-public-api.tinkoff.ru/rest"  # type: ignore
        self._client.headers = {"Authorization": f"Bearer {self._api_key}"}  # type: ignore
        logging.info("TinkoffInvestClient initialized")

    async def get_stock_info(self, ticker: str, timestamp: date | None = None) -> dict | None:
        logging.info(f"Searching stock ID by ticker '{ticker}'")
        route = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/FindInstrument"
        logging.info(f"Route '{route}' built")
        json = {
            "query": ticker,
            "instrumentKind": "INSTRUMENT_TYPE_SHARE",
            "apiTradeAvailableFlag": "true",
        }
        response = await self._post(route=route, json=json)
        if response is None:
            logging.info("Empty response, returning None")
            return None

        instruments: list | None = response.get("instruments", None)
        if instruments is None or len(instruments) == 0:
            logging.info("Not enough data in response, returning None")
            return None

        ticker_id = instruments[0].get("uid", None)
        ticker_name = instruments[0].get("name", None)

        if ticker_id is None or ticker_name is None:
            logging.info("Not enough data in response, returning None")
            return None

        logging.info(f"Stock ID for ticker '{ticker}' is '{ticker_id}'")
        logging.info(
            f"Trying to fetch stock information by ticker ID '{ticker_id}' and timestamp '{timestamp}'"
        )

        if timestamp is None:
            logging.info(
                "No timestamp provided, building request to fetch current ticker information"
            )
            route = "/tinkoff.public.invest.api.contract.v1.MarketDataService/GetLastPrices"
            json: dict[str, Any] = {"instrumentId": [ticker_id]}
            prices_target = "lastPrices"
            price_object_name = "price"
        else:
            logging.info("Timestamp provided, building request to fetch ticker information by date")
            route = "/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"
            from_date = f"{timestamp.strftime("%Y-%m-%d")}T00:00:00Z"
            to_timestamp = timestamp + timedelta(days=1)
            to_date = f"{to_timestamp.strftime("%Y-%m-%d")}T00:00:00Z"
            json: dict[str, Any] = {
                "from": from_date,
                "to": to_date,
                "interval": "CANDLE_INTERVAL_DAY",
                "instrumentId": ticker_id,
            }
            prices_target = "candles"
            price_object_name = "close"

        logging.info("Request built")
        response = await self._post(route=route, json=json)
        if response is None:
            logging.info("Empty response, returning None")
            return None
        prices: list = response.get(prices_target, [])
        if len(prices) == 0:
            logging.info("Not enough data in response, returning None")
            return None
        price_object = prices[0].get(price_object_name, {})

        units = price_object.get("units", None)
        nano = price_object.get("nano", None)
        if units is None or nano is None:
            logging.info("Not enough data in response, returning None")
            return None

        price = float(units) + float(nano) * 0.000000001

        logging.info("Returning all fetched stock information")
        return {
            "id": ticker_id,
            "name": ticker_name,
            "timestamp": date.today() if timestamp is None else timestamp,
            "price": price,
        }
