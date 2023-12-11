import asyncio

from src.clients.cryptocurrency_client import CoinGeckoClient
from src.clients.stock_client import TinkoffInvestClient
from utils.http_client import HttpClient


async def main():
    http_client = HttpClient()
    cg_client = CoinGeckoClient()
    ti_client = TinkoffInvestClient(http_client)
    print("Hello World!")


if __name__ == "__main__":
    asyncio.run(main())
