from datetime import date
from datetime import datetime


def to_float(text: str) -> float | None:
    try:
        result = float(text)
        return result
    except ValueError:
        return None


def to_date(text: str) -> date | None:
    try:
        result = datetime.strptime(text, "%d-%m-%Y")
        return result
    except (ValueError, TypeError):
        return None
