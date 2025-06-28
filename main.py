from flask import Flask, render_template, request
from oanda_handler import get_candles_from_oanda
from signal_logic import analyze_signals

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    signal_data = None
    if request.method == "POST":
        pair = request.form["pair"]
        interval = request.form.get("interval", "M15")
        candles = get_candles_from_oanda(pair, interval)
        if candles:
            signal_data = analyze_signals(candles)
            signal_data["pair"] = pair
            signal_data["interval"] = interval
    return render_template("index.html", signal=signal_data)

if __name__ == "__main__":
    app.run(debug=True)