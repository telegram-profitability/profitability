import asyncio

from clients.cryptocurrency_client import CoinGeckoClient


async def main():
    cg_client = CoinGeckoClient()
    print("Hello World!")


if __name__ == "__main__":
    asyncio.run(main())
