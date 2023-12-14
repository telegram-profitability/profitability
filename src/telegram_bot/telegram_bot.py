import logging
from uuid import uuid4

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
from src.telegram_bot import texts
from src.telegram_bot.texts import ERROR_TEXT
from src.telegram_bot.utils import to_date
from src.telegram_bot.utils import to_float

_cryptocurrency_client: AbstractCryptocurrencyClient | None = None
_stock_client: AbstractStockClient | None = None
_db: AbstractDatabase | None = None
_router = Router()
_bot = Bot(token=TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
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
    await _dp.start_polling(_bot)


@_router.message(Command("start", "help"))
async def start_handler(message: Message) -> None:
    await message.answer(texts.START_TEXT)


@_router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    message_user = message.from_user
    if message_user is None:
        await message.answer(texts.USER_FETCH_ERROR_TEXT)
        return

    user = {"id": message_user.id, "full_name": message_user.full_name}
    await _db.add_user(user)

    investments = await _db.get_all_investments(message_user.id)

    stock_tickers = [i["ticker"] for i in investments["stocks"]]
    current_stock_prices = {}
    for i in stock_tickers:
        stock_info = await _stock_client.get_stock_info(i)
        if stock_info is not None:
            current_stock_prices[i] = stock_info["price"]

    coin_tickers = [i["ticker"] for i in investments["coins"]]
    current_coin_prices = {}
    for i in coin_tickers:
        coin_info = await _cryptocurrency_client.get_coin_info(i)
        if coin_info is not None:
            current_coin_prices[i] = coin_info["price"]

    stock_stats = {i: 0 for i in stock_tickers}
    for investment in investments["stocks"]:
        ticker = investment["ticker"]
        amount = investment["amount"]
        initial_investment = amount * investment["price"]
        current_price = current_stock_prices.get(ticker)
        if current_price is None:
            continue
        current_value = amount * current_price
        profit_loss = current_value - initial_investment
        stock_stats[ticker] += profit_loss

    coin_stats = {i: 0 for i in coin_tickers}
    for investment in investments["coins"]:
        ticker = investment["ticker"]
        amount = investment["amount"]
        initial_investment = amount * investment["price"]
        current_price = current_coin_prices.get(ticker)
        if current_price is None:
            continue
        current_value = amount * current_price
        profit_loss = current_value - initial_investment
        coin_stats[ticker] += profit_loss

    stock_result = ["Stock:"]
    for k, v in stock_stats.items():
        stock_result.append(f"  - {k.upper()}: {"+" if v >= 0 else ""}{v:.2f}")

    coin_result = ["Coin:"]
    for k, v in coin_stats.items():
        coin_result.append(f"  - {k.upper()}: {"+" if v >= 0 else ""}{v:.2f}")

    result = []
    if len(stock_result) > 1:
        result.extend(stock_result)
    if len(coin_result) > 1:
        result.extend(coin_result)

    await message.answer("\n".join(result))


@_router.message(Command("stock"))
async def stock_handler(message: Message, command: Command) -> None:
    command_args = command.args  # type: ignore
    if command_args is None:
        await message.answer(ERROR_TEXT)
        return
    args = command_args.split()
    if len(args) not in [2, 3]:
        await message.answer(ERROR_TEXT)
        return

    ticker = args[0]
    if not ticker.isalpha():
        await message.answer(ERROR_TEXT)
        return
    ticker = ticker.lower()

    amount = to_float(args[1])
    if amount is None:
        await message.answer(ERROR_TEXT)
        return

    if len(args) != 3:
        timestamp = None
    else:
        timestamp = to_date(args[2])
        if timestamp is None:
            await message.answer(ERROR_TEXT)
            return

    message_user = message.from_user
    if message_user is None:
        await message.answer(texts.USER_FETCH_ERROR_TEXT)
        return

    user = {"id": message_user.id, "full_name": message_user.full_name}
    await _db.add_user(user)

    stock = await _stock_client.get_stock_info(ticker, timestamp)
    if stock is None:
        await message.answer(texts.OPERATION_ERROR_TEXT)
        return

    stock_entity = {
        "id": uuid4(),
        "name": stock["name"],
        "ticker": stock["ticker"],
        "amount": amount,
        "price": stock["price"],
        "timestamp": stock["timestamp"],
    }
    await _db.add_stock(stock_entity, message_user.id)
    await message.answer(texts.OPERATION_COMPLETED_TEXT)


@_router.message(Command("coin"))
async def coin_handler(message: Message, command: Command) -> None:
    command_args = command.args  # type: ignore
    if command_args is None:
        await message.answer(ERROR_TEXT)
        return
    args = command_args.split()
    if len(args) not in [2, 3]:
        await message.answer(ERROR_TEXT)
        return

    coin_id = args[0]
    if not coin_id.isalpha():
        await message.answer(ERROR_TEXT)
        return
    coin_id = coin_id.lower()

    amount = to_float(args[1])
    if amount is None:
        await message.answer(ERROR_TEXT)
        return

    if len(args) != 3:
        timestamp = None
    else:
        timestamp = to_date(args[2])
        if timestamp is None:
            await message.answer(ERROR_TEXT)
            return

    message_user = message.from_user
    if message_user is None:
        await message.answer(texts.USER_FETCH_ERROR_TEXT)
        return

    user = {"id": message_user.id, "full_name": message_user.full_name}
    await _db.add_user(user)

    coin = await _cryptocurrency_client.get_coin_info(coin_id, timestamp)
    if coin is None:
        await message.answer(texts.OPERATION_ERROR_TEXT)
        return

    coin_entity = {
        "id": uuid4(),
        "name": coin["name"],
        "symbol": coin_id,
        "amount": amount,
        "price": coin["price"],
        "timestamp": coin["timestamp"],
    }
    await _db.add_coin(coin_entity, message_user.id)
    await message.answer(texts.OPERATION_COMPLETED_TEXT)


@_router.message()
async def message_handler(message: Message) -> None:
    await message.answer(ERROR_TEXT)
