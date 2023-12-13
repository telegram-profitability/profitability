import asyncio
import logging
import os
import sys

from configs import LOG_FILE_NAME
from configs import TEMP_DIRECTORY_NAME
from src.clients.cryptocurrency_client import CoinGeckoClient
from src.clients.stock_client import TinkoffInvestClient


async def main():
    temp_directory_path = f"./{TEMP_DIRECTORY_NAME}"
    if not os.path.exists(temp_directory_path):
        os.makedirs(temp_directory_path)
    logging.basicConfig(
        level=logging.INFO,
        format='{timestamp="%(asctime)s", log_level="%(levelname)s", module="%(module)s", message="%(message)s"}',
        handlers=[
            logging.FileHandler(f"{temp_directory_path}/{LOG_FILE_NAME}", mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.info("Initializing application")
    cg_client = CoinGeckoClient()
    ti_client = TinkoffInvestClient()
    logging.info("Running application")


if __name__ == "__main__":
    asyncio.run(main())
