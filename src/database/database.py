from abc import ABC
from abc import abstractmethod
import logging
from typing import Any

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
    async def get_all_investments(self, user_id: int) -> dict[str, list[dict[str, Any]]]:
        raise NotImplementedError()


class PostgresDatabase(AbstractDatabase):
    def __init__(self) -> None:
        self._connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        logging.info("PostgresDatabase initialized")

    async def create_tables(self) -> None:
        logging.info("Creating database tables method called")
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
        logging.info("All tables created")

    async def add_user(self, user: dict[str, Any]) -> None:
        logging.info("Adding user to database")
        connection = await asyncpg.connect(self._connection_string)
        await connection.execute(
            """INSERT INTO "users"("id", "full_name") VALUES ($1, $2) ON CONFLICT (id) DO NOTHING""",
            user["id"],
            user["full_name"],
        )
        await connection.close()
        logging.info("User added to database")

    async def add_stock(self, stock: dict[str, Any], user_id: int) -> None:
        logging.info("Adding stock to database")
        connection = await asyncpg.connect(self._connection_string)
        await connection.execute(
            """INSERT INTO "stocks"(id, name, ticker, amount, price, timestamp, user_id) VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            stock["id"],
            stock["name"],
            stock["ticker"],
            stock["amount"],
            stock["price"],
            stock["timestamp"],
            user_id,
        )
        await connection.close()
        logging.info("Stock added to database")

    async def add_coin(self, coin: dict[str, Any], user_id: int) -> None:
        logging.info("Adding coin to database")
        connection = await asyncpg.connect(self._connection_string)
        await connection.execute(
            """INSERT INTO "coins"(id, name, ticker, amount, price, timestamp, user_id) VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            coin["id"],
            coin["name"],
            coin["symbol"],
            coin["amount"],
            coin["price"],
            coin["timestamp"],
            user_id,
        )
        await connection.close()
        logging.info("Coin added to database")

    async def get_all_investments(self, user_id: int) -> dict[str, list[dict[str, Any]]]:
        logging.info(f"Getting all stocks and coins of user with ID {user_id}")
        connection = await asyncpg.connect(self._connection_string)
        stocks_records = await connection.fetch(
            """SELECT * FROM stocks WHERE user_id = $1""", user_id
        )
        coins_records = await connection.fetch(
            """SELECT * FROM coins WHERE user_id = $1""", user_id
        )
        await connection.close()
        logging.info(f"Returning stocks and coins of user with ID {user_id} collected")
        return {
            "stocks": [dict(i) for i in stocks_records],
            "coins": [dict(i) for i in coins_records],
        }
