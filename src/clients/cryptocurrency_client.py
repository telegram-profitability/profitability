from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

import httpx

from src.configs import CG_API_KEY


class AbstractCryptocurrencyClient(ABC):
    _client = httpx.AsyncClient()

    @abstractmethod
    async def get_coin_info(self, coin_id: str, date: str = None) -> dict | None:
        raise NotImplementedError()

    async def _get(self, route: str, params: dict = None) -> dict | None:
        response = await self._client.get(url=route, params=params)
        return response.json() if response.status_code == 200 else None


class CoinGeckoClient(AbstractCryptocurrencyClient):
    def __init__(self) -> None:
        self._api_key = CG_API_KEY
        self._client.base_url = "https://api.coingecko.com/api"
        self._client.params = {"x_cg_api_key": self._api_key}
        self._currency = "rub"

    async def get_coin_info(self, coin_id: str, date: datetime = None) -> dict | None:
        route = f"/v3/coins/{coin_id}" if date is None else f"/v3/coins/{coin_id}/history"
        params = {} if date is None else {"date": date.strftime("%d-%m-%Y")}
        response = await self._get(route=route, params=params)
        if response is None:
            return None

        all_prices = response.get("market_data", {}).get("current_price", {})
        symbol: str | None = response.get("symbol", None)
        name: str | None = response.get("name", None)
        price: str | None = all_prices.get("rub", None)

        if symbol is None or name is None or price is None:
            return None

        return {
            "symbol": symbol,
            "name": name,
            "time": datetime.now(timezone.utc) if date is None else date,
            "price": float(price),
        }
