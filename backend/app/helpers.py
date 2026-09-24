from app.constants import SUPPORTED_SYMBOLS
from datetime import datetime, timezone
from typing import Optional


def to_number(value):
    if value in (None, "None", ""):
        return None

    return float(value)


def is_in_symbol(symbol):
    symbols = {s.lower() for s in SUPPORTED_SYMBOLS}
    status = symbol.lower() in symbols
    return status



def normalize_massive_prices(data):
    prices = []

    for item in data:

        timestamp = item["t"]

        date = datetime.fromtimestamp(
            timestamp / 1000,
            tz=timezone.utc
        ).date()

        prices.append({
            "date": date,
            "open": item.get("o"),
            "high": item.get("h"),
            "low": item.get("l"),
            "close": item.get("c"),
            "volume": item.get("v"),
            "vwap": item.get("vw"),
        })

    return prices

def percentage_change(previous_close, latest_close):

    if previous_close is None or previous_close == 0:
        return None

    return (
        (latest_close - previous_close)
        / previous_close
    ) * 100




def normalize_name(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    return " ".join(value.strip().split()).title()