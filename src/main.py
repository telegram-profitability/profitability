import asyncio
import logging
import os
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from configs import LOG_FILE_NAME
from configs import TEMP_DIRECTORY_NAME
from configs import TG_BOT_TOKEN
from handlers import router
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

    bot = Bot(token=TG_BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Running application")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
