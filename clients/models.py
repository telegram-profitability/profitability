from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CoinCurrentInfo:
    id: str
    symbol: str
    name: str
    time: datetime
    price: float
