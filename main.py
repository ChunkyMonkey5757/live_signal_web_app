import os
import logging
from flask import Flask, render_template
from api_handler import fetch_oanda_candles
from indicators import analyze_signals

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# ✅ Confirmed OANDA Crypto Pairs from User Screenshots
CRYPTO_PAIRS = [
    "BTC_USD", "ETH_USD", "LTC_USD", "BCH_USD",
    "LINK_USD", "SOL_USD", "UNI_USD", "PAXG_USD", "AAVE_USD"
]

@app.route("/")
def home():
    results = []

    for pair in CRYPTO_PAIRS:
        try:
            candles = fetch_oanda_candles(pair)
            signal = analyze_signals(candles)
            signal["pair"] = pair
            results.append(signal)
        except Exception as e:
            logging.exception(f"Failed to analyze {pair}")
            results.append({
                "pair": pair,
                "RSI": None,
                "MACD": None,
                "Signal Line": None,
                "Histogram": None,
                "ADX": None,
                "decision": "ERROR"
            })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("DEBUG", "False").lower() == "true"
    )
