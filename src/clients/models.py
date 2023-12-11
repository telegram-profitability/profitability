from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StockCurrentInfo:
    ticker: str
    name: str
    time: datetime
    price: float
