# LiveTradingBotWebApp

This is a full-stack, real-time trading assistant powered by live OANDA data and technical indicators (RSI, MACD, ADX). It delivers trading signals through a clean, mobile-ready web interface.

## ✅ Features
- Real-time candle data from OANDA REST API
- Signal generation using RSI, MACD, and ADX
- Web-based UI with mobile/tablet support
- Flask backend with REST API and HTML rendering
- Easy deployment on Railway, Replit, or local server

## 📦 Tech Stack
- Python 3
- Flask
- Requests
- dotenv

## 🚀 Deployment

### Railway
1. Push this repo to GitHub
2. Go to [Railway](https://railway.app) → New Project → Deploy from GitHub
3. Set the following environment variables:
    - `OANDA_API_KEY=your-demo-api-key`
    - `OANDA_ACCOUNT_TYPE=practice`
    - `PORT=5000`
    - `DEBUG=False`
4. Set start command: `python main.py` (if needed)

### Local
```bash
pip install -r requirements.txt
cp .env.example .env  # fill in your keys
python main.py
```

## 📁 Project Structure
```
main.py                # Flask app entry point
api_handler.py         # OANDA API integration
indicators.py          # RSI, MACD, ADX logic
frontend/index.html    # Mobile-friendly UI
requirements.txt       # Dependencies
.env.example           # Env variable template
```

## 📘 License
MIT License — free to use and extend.
