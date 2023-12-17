import logging
from uuid import uuid4

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import *

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


# user_data = {}


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
    await Bot.set_my_commands(self=_bot,
                              commands=[BotCommand(command='stats', description='📊 Просмотр своего портфеля'),
                                        BotCommand(command='add', description='➕ Добавить покупку или продажу'),
                                        BotCommand(command='help', description='❔ Помощь')])


@_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(texts.START_TEXT)


@_dp.message(Command("help"))
async def start_handler(message: Message) -> None:
    await message.reply(texts.HELP_TEXT)


@_dp.message(Command("add"))
async def add_new_item(message: Message) -> None:
    add_stock_button = InlineKeyboardButton(text='Ценной бумаги', callback_data='stock')
    add_cryptocurrency_button = InlineKeyboardButton(text='Криптовалюты', callback_data='crypto')
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[add_stock_button, add_cryptocurrency_button]])
    await message.answer('➕ Добавить покупку или продажу...', reply_markup=inline_keyboard)


@_dp.callback_query(lambda query: query.data in ['stock', 'crypto'])
async def process_adding_new_item(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    chosen_option = callback_query.data
    if chosen_option == 'stock':
        # user_data[callback_query.from_user.id] = {'chosen_option': 'add_stock'}
        await _bot.send_message(callback_query.from_user.id, texts.ADD_STOCK_TEXT, parse_mode='MarkdownV2')
    elif chosen_option == 'crypto':
        # user_data[callback_query.from_user.id] = {'chosen_option': 'add_crypto'}
        await _bot.send_message(callback_query.from_user.id, texts.ADD_CRYPTO_TEXT, parse_mode='MarkdownV2')


# @_dp.message(lambda message: message.from_user.id in user_data and user_data[message.from_user.id]['chosen_option'] == 'add_crypto')
# async def process_adding_new_crypto(message: Message) -> None:
#     cryptocurrency_input = message.text
#     if not cryptocurrency_input.isalpha():
#         await message.reply(ERROR_TEXT)
#         return
#     cryptocurrency = cryptocurrency_input.lower()
#     user_data[message.from_user.id]['add_cryptocurrency'] = cryptocurrency
#     await message.reply("Введи количество купленной валюты (например, 3.2).\nЕсли ты продал валюту, значение должно быть отрицательным (например, -1)")
#
#
# @_dp.message(lambda message: message.from_user.id in user_data and 'add_cryptocurrency' in user_data[message.from_user.id])
# async def process_adding_new_crypto_amount(message: Message) -> None:
#     cryptocurrency_amount_input = message.text
#     cryptocurrency_amount = to_float(cryptocurrency_amount_input)
#     if cryptocurrency_amount is None:
#         await message.reply(ERROR_TEXT)
#         return
#     user_data[message.from_user.id]['add_cryptocurrency_amount'] = cryptocurrency_amount
#     await message.reply(
#         "Введи дату покупки или продажи в формате DD-MM-YYYY (например, 12-11-2020).\nЕсли операция была сделана сегодня, можно ответить «Сегодня»")
#
#
# @_dp.message(lambda message: message.from_user.id in user_data and 'add_cryptocurrency_amount' in user_data[message.from_user.id])
# async def process_adding_new_crypto_date(message: Message) -> None:
#     cryptocurrency_date_input = message.text
#     if cryptocurrency_date_input == 'Сегодня':
#         cryptocurrency_date = None
#     else:
#         cryptocurrency_date = to_date(cryptocurrency_date_input)
#         if cryptocurrency_date is None:
#             await message.reply(ERROR_TEXT)
#             return
#     message_user = message.from_user
#     if message_user is None:
#         await message.reply(texts.USER_FETCH_ERROR_TEXT)
#         return
#
#     user = {"id": message_user.id, "full_name": message_user.full_name}
#     await _db.add_user(user)
#     coin_id = user_data[message.from_user.id]['add_cryptocurrency']
#     amount = user_data[message.from_user.id]['add_cryptocurrency_amount']
#     timestamp = cryptocurrency_date
#     coin = await _cryptocurrency_client.get_coin_info(coin_id, timestamp)
#     if coin is None:
#         await message.reply(texts.OPERATION_ERROR_TEXT)
#         return
#
#     coin_entity = {
#         "id": uuid4(),
#         "name": coin["name"],
#         "symbol": coin_id,
#         "amount": amount,
#         "price": coin["price"],
#         "timestamp": coin["timestamp"],
#     }
#     await _db.add_coin(coin_entity, message_user.id)
#     await message.reply(texts.OPERATION_COMPLETED_TEXT)

@_router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    message_user = message.from_user
    if message_user is None:
        await message.reply(texts.USER_FETCH_ERROR_TEXT)
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

    stock_result = ["📑 Ценные бумаги"]
    for k, v in stock_stats.items():
        stock_result.append(f"  - {k.upper()}: {'+' if v >= 0 else ''}{v:.2f} RUB")

    coin_result = ["🪙 Криптовалюта"]
    for k, v in coin_stats.items():
        coin_result.append(f"  - {k.upper()}: {'+' if v >= 0 else ''}{v:.2f} RUB")

    stock_and_coin = []
    if len(stock_result) > 1:
        stock_and_coin.extend(stock_result)
    if len(coin_result) > 1:
        stock_and_coin.extend(coin_result)

    result = "\n".join(stock_and_coin) if len(stock_and_coin) != 0 else texts.ADD_OPERATIONS
    result_message = f"📊 Твой портфель:\n\n{result}"
    await message.reply(result_message)


@_router.message(Command("stock"))
async def stock_handler(message: Message, command: Command) -> None:
    command_args = command.args  # type: ignore
    if command_args is None:
        await message.reply(ERROR_TEXT)
        return
    args = command_args.split()
    if len(args) not in [2, 3]:
        await message.reply(ERROR_TEXT)
        return

    ticker = args[0]
    if not ticker.isalpha():
        await message.reply(ERROR_TEXT)
        return
    ticker = ticker.lower()

    amount = to_float(args[1])
    if amount is None:
        await message.reply(ERROR_TEXT)
        return

    if len(args) != 3:
        timestamp = None
    else:
        timestamp = to_date(args[2])
        if timestamp is None:
            await message.reply(ERROR_TEXT)
            return

    message_user = message.from_user
    if message_user is None:
        await message.reply(texts.USER_FETCH_ERROR_TEXT)
        return

    user = {"id": message_user.id, "full_name": message_user.full_name}
    await _db.add_user(user)

    stock = await _stock_client.get_stock_info(ticker, timestamp)
    if stock is None:
        await message.reply(texts.OPERATION_ERROR_TEXT)
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
    await message.reply(texts.OPERATION_COMPLETED_TEXT)


@_router.message(Command("coin"))
async def coin_handler(message: Message, command: Command) -> None:
    command_args = command.args  # type: ignore
    if command_args is None:
        await message.reply(ERROR_TEXT)
        return
    args = command_args.split()
    if len(args) not in [2, 3]:
        await message.reply(ERROR_TEXT)
        return

    coin_id = args[0]
    if not coin_id.isalpha():
        await message.reply(ERROR_TEXT)
        return
    coin_id = coin_id.lower()

    amount = to_float(args[1])
    if amount is None:
        await message.reply(ERROR_TEXT)
        return

    if len(args) != 3:
        timestamp = None
    else:
        timestamp = to_date(args[2])
        if timestamp is None:
            await message.reply(ERROR_TEXT)
            return

    message_user = message.from_user
    if message_user is None:
        await message.reply(texts.USER_FETCH_ERROR_TEXT)
        return

    user = {"id": message_user.id, "full_name": message_user.full_name}
    await _db.add_user(user)

    coin = await _cryptocurrency_client.get_coin_info(coin_id, timestamp)
    if coin is None:
        await message.reply(texts.OPERATION_ERROR_TEXT)
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
    await message.reply(texts.OPERATION_COMPLETED_TEXT)


@_router.message()
async def message_handler(message: Message) -> None:
    await message.reply(ERROR_TEXT)
