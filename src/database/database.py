from abc import ABC
from abc import abstractmethod
import logging
from typing import Any
from uuid import uuid4

import asyncpg  # type: ignore

from src.configs import POSTGRES_DB
from src.configs import POSTGRES_HOST
from src.configs import POSTGRES_PASSWORD
from src.configs import POSTGRES_PORT
from src.configs import POSTGRES_USER


class AbstractDatabase(ABC):
    @abstractmethod
    async def create_tables(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def add_user(self, user: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def add_stock(self, stock: dict[str, Any], user_id: int) -> None:
        raise NotImplementedError()

    async def add_coin(self, coin: dict[str, Any], user_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_all_investments(self, user_id: int) -> dict[str, list[dict[str, str]]]:
        raise NotImplementedError()


class PostgresDatabase(AbstractDatabase):
    def __init__(self) -> None:
        self._connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        logging.info(self._connection_string)

    async def create_tables(self) -> None:
        connection = await asyncpg.connect(self._connection_string)
        async with connection.transaction():
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS "coins"(
                    "id" UUID PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "ticker" TEXT NOT NULL,
                    "amount" INTEGER NOT NULL,
                    "price" FLOAT NOT NULL,
                    "timestamp" DATE NOT NULL,
                    "user_id" INTEGER NOT NULL
                )"""
            )
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS "stocks"(
                    "id" UUID PRIMARY KEY,
                    "name" TEXT NOT NULL,
                    "ticker" TEXT NOT NULL,
                    "amount" INTEGER NOT NULL,
                    "price" FLOAT NOT NULL,
                    "timestamp" DATE NOT NULL,
                    "user_id" INTEGER NOT NULL
                )"""
            )
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS "users"(
                    "id" INTEGER NOT NULL PRIMARY KEY,
                    "full_name" TEXT NOT NULL
                )"""
            )
        await connection.close()

    async def add_user(self, user: dict[str, Any]) -> None:
        connection = await asyncpg.connect(self._connection_string)
        await connection.execute(
            """INSERT INTO "users"("id", "full_name") VALUES ($1, $2)""",
            user["id"],
            user["full_name"],
        )
        await connection.close()

    async def add_stock(self, stock: dict[str, Any], user_id: int) -> None:
        connection = await asyncpg.connect(self._connection_string)
        await connection.execute(
            """INSERT INTO "stocks"(id, name, ticker, amount, price, timestamp, user_id) VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            uuid4(),
            stock["name"],
            stock["ticker"],
            stock["amount"],
            stock["price"],
            stock["timestamp"],
            user_id,
        )
        await connection.close()

    async def add_coin(self, coin: dict[str, Any], user_id: int) -> None:
        connection = await asyncpg.connect(self._connection_string)
        await connection.execute(
            """INSERT INTO "coins"(id, name, ticker, amount, price, timestamp, user_id) VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            uuid4(),
            coin["name"],
            coin["symbol"],
            coin["amount"],
            coin["price"],
            coin["timestamp"],
            user_id,
        )
        await connection.close()

    async def get_all_investments(self, user_id: int) -> dict[str, list[dict[str, str]]]:
        connection = await asyncpg.connect(self._connection_string)
        stocks_records = await connection.fetch(
            """SELECT * FROM stocks WHERE user_id = $1""", user_id
        )
        coins_records = await connection.fetch(
            """SELECT * FROM coins WHERE user_id = $1""", user_id
        )
        await connection.close()
        return {
            "stocks": [dict(i) for i in stocks_records],
            "coins": [dict(i) for i in coins_records],
        }
