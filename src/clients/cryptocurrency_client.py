from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

from src.clients.models import CoinCurrentInfo
from src.configs import CG_API_KEY
from utils.http_client import AbstractHttpClient


class AbstractCryptocurrencyClient(ABC):
    @abstractmethod
    async def get_coin_current_info(self, coin: str) -> CoinCurrentInfo | None:
        raise NotImplementedError()


class CoinGeckoClient(AbstractCryptocurrencyClient):
    def __init__(self, client: AbstractHttpClient) -> None:
        self._api_key = CG_API_KEY
        self._client = client

    async def get_coin_current_info(self, coin: str) -> CoinCurrentInfo | None:
        params = {
            "vs_currencies": "rub",
            "x_cg_api_key": self._api_key,
        }
        response = await self._client.get(
            url=f"https://api.coingecko.com/api/v3/coins/{coin}", params=params
        )
        if response is None:
            return None

        all_prices = response.get("market_data", {}).get("current_price", {})
        coin_id: str | None = response.get("id", None)
        symbol: str | None = response.get("symbol", None)
        name: str | None = response.get("name", None)
        price: str | None = all_prices.get("rub", None)

        if any(i is None for i in [coin_id, symbol, name, price]):
            return None

        return CoinCurrentInfo(
            id=coin_id,
            symbol=symbol,
            name=name,
            time=datetime.now(timezone.utc),
            price=float(price),
        )
