import requests
import os

OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT_TYPE = os.getenv("OANDA_ACCOUNT_TYPE", "practice")
OANDA_BASE_URL = f"https://api-{OANDA_ACCOUNT_TYPE}.oanda.com/v3"

def get_candles_from_oanda(pair, granularity="M15", count=100):
    url = f"{OANDA_BASE_URL}/instruments/{pair}/candles"
    headers = {"Authorization": f"Bearer {OANDA_API_KEY}"}
    params = {"count": count, "granularity": granularity, "price": "M"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        candles = [{
            "time": c["time"],
            "open": float(c["mid"]["o"]),
            "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]),
            "close": float(c["mid"]["c"])
        } for c in data["candles"] if c["complete"]]
        return candles
    else:
        print("Error fetching candles:", response.status_code, response.text)
        return None