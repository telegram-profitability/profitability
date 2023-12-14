import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from src.clients.cryptocurrency_client import AbstractCryptocurrencyClient
from src.clients.stock_client import AbstractStockClient
from src.configs import TG_BOT_TOKEN
from src.database.database import AbstractDatabase


_cryptocurrency_client: AbstractCryptocurrencyClient | None = None
_stock_client: AbstractStockClient | None = None
_db: AbstractDatabase | None = None
_router = Router()
_bot = Bot(token=TG_BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
_dp = Dispatcher(storage=MemoryStorage())
_dp.include_router(_router)


def init_bot(
    cryptocurrency_client: AbstractCryptocurrencyClient,
    stock_client: AbstractStockClient,
    db: AbstractDatabase,
) -> None:
    global _cryptocurrency_client, _stock_client, _db
    _cryptocurrency_client = cryptocurrency_client
    _stock_client = stock_client
    _db = db
    logging.info("Telegram bot initialized")


async def run_bot() -> None:
    logging.info("Telegram bot run method called")
    await _db.create_tables()  # type: ignore
    await _bot.delete_webhook(drop_pending_updates=True)
    await _dp.start_polling()


@_router.message(Command("start"))
async def start_handler(msg: Message) -> None:
    await msg.answer("Я могу помочь тебе узнать твой ID, просто отправь мне любое сообщение")


@_router.message()
async def message_handler(msg: Message) -> None:
    if msg.from_user is None:
        await msg.answer("Can't identify your ID")
    else:
        await msg.answer(f"Your ID: {msg.from_user.id}")
