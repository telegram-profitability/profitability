from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

import httpx

from clients.models import CoinCurrentInfo
from configs import CG_API_KEY


class AbstractCryptocurrencyClient(ABC):
    @abstractmethod
    async def get_current_coin_info(self, coin: str) -> CoinCurrentInfo | None:
        raise NotImplementedError()


class CoinGeckoClient(AbstractCryptocurrencyClient):
    def __init__(self) -> None:
        self.api_key = CG_API_KEY

    async def get_current_coin_info(self, coin: str) -> CoinCurrentInfo | None:
        parameters = {
            "vs_currencies": "rub",
            "x_cg_api_key": self.api_key,
        }
        response_json = None
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"https://api.coingecko.com/api/v3/coins/{coin}",
                params=parameters,
            )
            if response.status_code == 200:
                response_json = response.json()

        if response_json is None:
            return None

        all_prices = response_json.get("market_data", {}).get("current_price", {})
        coin_id = response_json.get("id")
        symbol = response_json.get("symbol")
        name = response_json.get("name")
        price = all_prices.get("rub")

        if any(i is None for i in [coin_id, symbol, name, price]):
            return None

        return CoinCurrentInfo(
            id=coin_id,
            symbol=symbol,
            name=name,
            time=datetime.now(timezone.utc),
            price=price
        )