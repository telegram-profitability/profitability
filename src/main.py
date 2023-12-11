import asyncio

from src.clients.cryptocurrency_client import CoinGeckoClient
from src.clients.stock_client import TinkoffInvestClient


async def main():
    cg_client = CoinGeckoClient()
    ti_client = TinkoffInvestClient()
    print("Hello World!")


if __name__ == "__main__":
    asyncio.run(main())
