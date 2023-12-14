import asyncio
import logging
import os
import sys

from src.database.database import PostgresDatabase
from src.configs import LOG_FILE_NAME
from src.configs import TEMP_DIRECTORY_NAME
from src.clients.cryptocurrency_client import CoinGeckoClient
from src.clients.stock_client import TinkoffInvestClient
from src.telegram_bot.telegram_bot import init_bot
from src.telegram_bot.telegram_bot import run_bot


async def app() -> None:
    logging.info("Initializing application")
    cg_client = CoinGeckoClient()
    ti_client = TinkoffInvestClient()
    db = PostgresDatabase()
    init_bot(cg_client, ti_client, db)

    logging.info("Creating database tables")
    await db.create_tables()
    logging.info("Running application")
    await run_bot()


def main() -> None:
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
    asyncio.run(app())


if __name__ == "__main__":
    main()
