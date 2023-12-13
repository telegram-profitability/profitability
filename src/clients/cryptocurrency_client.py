from abc import ABC
from abc import abstractmethod
from datetime import date
import logging

import httpx

from src.configs import CG_API_KEY


class AbstractCryptocurrencyClient(ABC):
    _client = httpx.AsyncClient()

    @abstractmethod
    async def get_coin_info(self, coin_id: str, timestamp: date = None) -> dict | None:
        raise NotImplementedError()

    async def _get(self, route: str, params: dict = None) -> dict | None:
        logging.info("Sending GET request to cryptocurrency API")
        response = await self._client.get(url=route, params=params)
        logging.info("Response received")
        if response.status_code == 200:
            logging.info("Response status code is 200, returning dictionary")
            return response.json()
        logging.info(f"Response status code is {response.status_code}, returning None")
        return None


class CoinGeckoClient(AbstractCryptocurrencyClient):
    def __init__(self) -> None:
        self._api_key = CG_API_KEY
        self._client.base_url = "https://api.coingecko.com/api"
        self._client.params = {"x_cg_api_key": self._api_key}
        self._currency = "rub"
        logging.info("CoinGeckoClient initialized")

    async def get_coin_info(self, coin_id: str, timestamp: date = None) -> dict | None:
        logging.info(f"Trying to fetch coin information by coin id '{coin_id}' and timestamp '{timestamp}'")
        route = f"/v3/coins/{coin_id}" if timestamp is None else f"/v3/coins/{coin_id}/history"
        logging.info(f"Route '{route}' built")
        params = {} if timestamp is None else {"date": timestamp.strftime("%d-%m-%Y")}
        response = await self._get(route=route, params=params)
        if response is None:
            logging.info("Empty response, returning None")
            return None

        all_prices = response.get("market_data", {}).get("current_price", {})
        symbol: str | None = response.get("symbol", None)
        name: str | None = response.get("name", None)
        price: str | None = all_prices.get("rub", None)

        if symbol is None or name is None or price is None:
            logging.info("Not enough data in response, returning None")
            return None

        logging.info("Returning all fetched coin information")
        return {
            "symbol": symbol,
            "name": name,
            "timestamp": date.today() if timestamp is None else timestamp,
            "price": float(price),
        }
