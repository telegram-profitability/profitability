import asyncio
import logging
import os
import sys

from configs import LOG_FILE_NAME
from configs import TEMP_DIRECTORY_NAME
from src.clients.cryptocurrency_client import CoinGeckoClient
from src.clients.stock_client import TinkoffInvestClient


async def main():
    if not os.path.exists(f"./{TEMP_DIRECTORY_NAME}"):
        os.makedirs(f"./{TEMP_DIRECTORY_NAME}")
    logging.basicConfig(
        level=logging.INFO,
        format="{timestamp=\"%(asctime)s\", log_level=\"%(levelname)s\", message=\"%(message)s\"}",
        handlers=[
            logging.FileHandler(f"./{TEMP_DIRECTORY_NAME}/{LOG_FILE_NAME}", mode="a"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    cg_client = CoinGeckoClient()
    ti_client = TinkoffInvestClient()
    logging.info("Running application")


if __name__ == "__main__":
    asyncio.run(main())
