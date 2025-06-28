import logging
from typing import List, Dict, Tuple

# Setup logger
logger = logging.getLogger(__name__)

def rsi(prices: List[float], period: int = 14) -> float:
    """Calculate RSI using Wilder's smoothing method."""
    if len(prices) <= period:
        raise ValueError("Not enough data to calculate RSI")

    gains, losses = [], []

    for i in range(1, period + 1):
        delta = prices[i] - prices[i - 1]
        gains.append(max(delta, 0))
        losses.append(abs(min(delta, 0)))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    for i in range(period + 1, len(prices)):
        delta = prices[i] - prices[i - 1]
        gain = max(delta, 0)
        loss = abs(min(delta, 0))

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def ema(prices: List[float], period: int) -> List[float]:
    """Exponential Moving Average for MACD/ADX smoothing."""
    ema_vals = [sum(prices[:period]) / period]
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema_vals.append((price - ema_vals[-1]) * multiplier + ema_vals[-1])
    return ema_vals


def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
    """Calculate MACD line, signal line, and histogram."""
    if len(prices) < slow + signal:
        raise ValueError("Not enough data for MACD")

    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)

    # Align lengths
    min_len = min(len(ema_fast), len(ema_slow))
    macd_line = [f - s for f, s in zip(ema_fast[-min_len:], ema_slow[-min_len:])]
    signal_line = ema(macd_line, signal)

    # Match histogram length to signal line
    hist = macd_line[-len(signal_line):]
    histogram = [m - s for m, s in zip(hist, signal_line)]

    return macd_line[-1], signal_line[-1], histogram[-1]


def adx(candles: List[Dict], period: int = 14) -> float:
    """Calculate Average Directional Index (ADX) using Wilder's method."""
    if len(candles) < period + 1:
        raise ValueError("Not enough data to calculate ADX")

    tr_list, plus_dm_list, minus_dm_list = [], [], []

    for i in range(1, len(candles)):
        current = candles[i]
        previous = candles[i - 1]

        high, low, close = current["high"], current["low"], previous["close"]
        prev_high, prev_low = previous["high"], previous["low"]

        tr = max(high - low, abs(high - close), abs(low - close))
        up_move = high - prev_high
        down_move = prev_low - low

        plus_dm = up_move if up_move > down_move and up_move > 0 else 0
        minus_dm = down_move if down_move > up_move and down_move > 0 else 0

        tr_list.append(tr)
        plus_dm_list.append(plus_dm)
        minus_dm_list.append(minus_dm)

    def smooth(values: List[float], period: int) -> List[float]:
        smoothed = [sum(values[:period])]
        for i in range(period, len(values)):
            smoothed.append(smoothed[-1] - (smoothed[-1] / period) + values[i])
        return smoothed

    atr = smooth(tr_list, period)
    sm_plus_dm = smooth(plus_dm_list, period)
    sm_minus_dm = smooth(minus_dm_list, period)

    plus_di = [(p / a) * 100 if a != 0 else 0 for p, a in zip(sm_plus_dm, atr)]
    minus_di = [(m / a) * 100 if a != 0 else 0 for m, a in zip(sm_minus_dm, atr)]
    dx = [abs(p - m) / (p + m) * 100 if (p + m) != 0 else 0 for p, m in zip(plus_di, minus_di)]

    adx_values = smooth(dx, period)
    return adx_values[-1]


def analyze_signals(candles: List[Dict]) -> Dict:
    """Combine RSI, MACD, ADX into a trade decision."""
    try:
        closes = [c["close"] for c in candles]
        rsi_val = rsi(closes)
        macd_line, signal_line, hist = macd(closes)
        adx_val = adx(candles)

        decision = "HOLD"
        if rsi_val < 30 and macd_line > signal_line and adx_val > 20:
            decision = "BUY"
        elif rsi_val > 70 and macd_line < signal_line and adx_val > 20:
            decision = "SELL"

        result = {
            "RSI": round(rsi_val, 2),
            "MACD": round(macd_line, 5),
            "Signal Line": round(signal_line, 5),
            "Histogram": round(hist, 5),
            "ADX": round(adx_val, 2),
            "decision": decision
        }

        logger.info(f"Signal analysis result: {result}")
        return result

    except Exception as e:
        logger.exception(f"Signal analysis failed: {str(e)}")
        return {
            "RSI": None,
            "MACD": None,
            "Signal Line": None,
            "Histogram": None,
            "ADX": None,
            "decision": "ERROR"
        }
