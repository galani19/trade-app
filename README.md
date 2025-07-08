# PrimeTrade Pro – Binance Futures Testnet Trading Bot

A modern, professional web-based trading bot for Binance USDT-M Futures Testnet, built with Python and Streamlit.

---

## Features

- Place market, limit, and stop-limit orders on Binance Futures Testnet
- Modern, responsive UI (Streamlit)
- Secure API key handling (Testnet only)
- Order validation, notional checks, and error handling
- Live price display for selected symbol
- Professional look and feel

---

## Setup Instructions

### 1. Clone or Download the Repository

```sh
git clone <your-repo-url>
```

### 2. Install Dependencies

Make sure you have Python 3.8+ installed.

```sh
pip install -r requirements.txt
```

### 3. Get Binance Futures Testnet API Keys

- Register/login at [Binance Futures Testnet](https://testnet.binancefuture.com)
- Generate API Key and Secret (ensure Futures permissions are enabled)

### 4. Run the Trading Bot Web App

```sh
streamlit run app.py
```

- The app will open in your browser (usually at http://localhost:8501)
- Enter your Testnet API Key and Secret in the UI (never use real/mainnet keys)
- Place trades using the web interface

---

## Files

- `app.py` – Main Streamlit web app (frontend)
- `basic_bot.py` – Trading logic and Binance API integration
- `requirements.txt` – Python dependencies

---

## Notes

- **Only use Binance Testnet API keys.** Never use real/mainnet keys.
- This app is for educational and testing purposes only.
- All logs are saved to `tradebot.log`.

---

## Troubleshooting

- If you see API key errors, double-check you are using Testnet keys and have enabled Futures permissions.
- If you see notional/precision errors, adjust your quantity and price to meet Binance Futures requirements.

---
