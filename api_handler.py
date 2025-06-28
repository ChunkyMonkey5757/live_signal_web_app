import os
import requests
from typing import List, Dict

OANDA_API_KEY = os.getenv("OANDA_API_KEY")
ACCOUNT_TYPE = os.getenv("OANDA_ACCOUNT_TYPE", "practice")
OANDA_URL = "https://api-fxtrade.oanda.com/v3/instruments"

HEADERS = {
    "Authorization": f"Bearer {OANDA_API_KEY}"
}

def fetch_oanda_candles(pair: str, count: int = 100) -> List[Dict]:
    """
    Fetch candle data from OANDA for a given instrument.
    """
    url = f"{OANDA_URL}/{pair}/candles"
    params = {
        "count": count,
        "granularity": "M5",
        "price": "M"
    }

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    candles = []
    for c in data["candles"]:
        candle = {
            "time": c["time"],
            "open": float(c["mid"]["o"]),
            "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]),
            "close": float(c["mid"]["c"]),
            "volume": c["volume"]
        }
        candles.append(candle)

    return candles
