from pydantic import BaseModel


class CoinPrice(BaseModel):
    currency: str
    price: float


class CoinInfo(BaseModel):
    id: str
    symbol: str
    name: str
    prices: list[CoinPrice]
