import streamlit as st
from basic_bot import BasicBot
from decimal import Decimal, ROUND_DOWN
from binance.client import Client
from binance.exceptions import BinanceAPIException
import time

st.set_page_config(
    page_title="PrimeTrade Pro - Binance Futures Trading", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Modern trending color palette and improved layout
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
        background: #f6f8fa !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    .main-header {
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
        padding: 28px 20px 18px 20px;
        margin: 0;
        color: #fff;
        text-align: center;
        border-radius: 0 0 18px 18px;
        box-shadow: 0 2px 24px rgba(6,182,212,0.08);
    }
    .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 32px 24px 18px 24px;
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 4px 32px rgba(99,102,241,0.08);
    }
    .trading-card {
        background: #000000;
        border-radius: 14px;
        padding: 28px 20px 18px 20px;
        box-shadow: 0 2px 12px rgba(6,182,212,0.07);
        border: 1px solid #e0e7ef;
        margin-bottom: 24px;
        max-width: 100%;
    }
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 18px;
        padding-bottom: 10px;
        border-bottom: 1px solid #e0e7ef;
    }
    .card-title {
        font-size: 19px;
        font-weight: 600;
        color: #000000;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .price-display {
        background: linear-gradient(90deg, #06b6d4 0%, #6366f1 100%);
        color: #fff;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        margin: 14px 0;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 2px 12px rgba(99,102,241,0.10);
    }
    .info-box {
        background: #e0f2fe;
        border-left: 4px solid #06b6d4;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 14px 0;
        color: #0369a1;
        font-size: 15px;
    }
    .notional-display {
        background: #f1f5f9;
        padding: 14px;
        border-radius: 8px;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        color: #334155;
        margin: 14px 0;
    }
    .success-card {
        background: #e0fce7 !important;
        border: 2px solid #22c55e !important;
        border-radius: 12px;
        padding: 18px;
        margin: 14px 0;
        color: #166534 !important;
        font-weight: 600;
        font-size: 18px;
        text-align: center;
    }
    .error-card {
        background: #fef2f2 !important;
        border: 2px solid #ef4444 !important;
        border-radius: 12px;
        padding: 18px;
        margin: 14px 0;
        color: #991b1b !important;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
    }
    .warning-card {
        background: #fef9c3 !important;
        border: 2px solid #eab308 !important;
        border-radius: 12px;
        padding: 18px;
        margin: 14px 0;
        color: #854d0e !important;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
    }
    .order-summary {
        background: #f8fafc !important;
        border-radius: 12px;
        padding: 18px;
        margin: 14px 0;
        color: #222 !important;
    }
    .order-summary table {
        width: 100%;
        border-collapse: collapse;
        background: #fff !important;
    }
    .order-summary th,
    .order-summary td {
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
        color: #222 !important;
        background: #fff !important;
    }
    .order-summary th {
        background: #e0e7ef !important;
        font-weight: 600;
        color: #334155 !important;
    }
    .footer {
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
        color: #fff;
        text-align: center;
        padding: 18px;
        margin-top: 32px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        border-radius: 12px;
        font-size: 15px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(6,182,212,0.13) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.18) !important;
    }
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #e0e7ef !important;
        font-size: 15px !important;
        max-width: 100% !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6,182,212,0.13) !important;
    }
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 30px; font-weight: 700;">⚡ PrimeTrade Pro</h1>
        <p style="margin: 8px 0 0 0; font-size: 16px; opacity: 0.93;">Modern Binance Futures Trading Platform</p>
    </div>
    <div style="height: 32px;"></div>
""", unsafe_allow_html=True)

# API Credentials Card
st.markdown("""
    <div class="trading-card">
        <div class="card-header">
            <h2 class="card-title">🔐 API Configuration</h2>
        </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <strong>🛡 Security Notice:</strong> This interface connects to Binance Futures <strong>Testnet</strong> only. 
        Your API credentials are processed securely and never stored.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    api_key = st.text_input("🔑 API Key", type="password", placeholder="Enter your Binance Testnet API Key")
with col2:
    api_secret = st.text_input("🔒 API Secret", type="password", placeholder="Enter your Binance Testnet API Secret")

st.markdown("</div>", unsafe_allow_html=True)

# Add extra space between API and Trading Interface sections
st.markdown('<div style="height: 38px;"></div>', unsafe_allow_html=True)

# Trading Interface Card
st.markdown("""
    <div class="trading-card">
        <div class="card-header">
            <h2 class="card-title">📊 Trading Interface</h2>
        </div>
""", unsafe_allow_html=True)

# Symbol and Price Display
col1, col2 = st.columns([2, 1])
with col1:
    symbol = st.text_input("📈 Trading Pair", value="BTCUSDT", placeholder="e.g., BTCUSDT, ETHUSDT")

# Fetch and display latest price
def get_latest_price(symbol):
    try:
        client = Client("", "")
        client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        ticker = client.futures_symbol_ticker(symbol=symbol.upper())
        return float(ticker['price'])
    except BinanceAPIException:
        return None
    except Exception:
        return None

latest_price = None
if symbol:
    latest_price = get_latest_price(symbol)
    if isinstance(latest_price, float):
        st.markdown(f"""
            <div class="price-display">
                💰 Current Price: <strong>{latest_price:,.1f} USDT</strong>
            </div>
        """, unsafe_allow_html=True)

# Order Configuration
st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    order_type = st.selectbox("📋 Order Type", ["market", "limit", "stop-limit"])
with col2:
    side = st.selectbox("🎯 Order Side", ["BUY", "SELL"])
with col3:
    quantity = st.number_input("📦 Quantity", min_value=0.001, step=0.001, format="%.3f")

# Price inputs based on order type
if order_type in ["limit", "stop-limit"]:
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("💵 Limit Price", min_value=0.0, step=0.1, format="%.1f")
    with col2:
        if order_type == "stop-limit":
            stop_price = st.number_input("🛑 Stop Price", min_value=0.0, step=0.1, format="%.1f")
        else:
            stop_price = None
else:
    price = None
    stop_price = None

# Trading Info Box
st.markdown("""
    <div class="info-box">
        <strong>💡 Trading Tips:</strong><br>
        • For <strong>BTCUSDT</strong>: Quantity step = 0.001, Price step = 0.1<br>
        • Minimum notional value: 100 USDT<br>
        • Market orders execute immediately at current market price
    </div>
""", unsafe_allow_html=True)

# Calculations and validations
def adjust_precision(val, precision):
    return float(Decimal(val).quantize(Decimal(precision), rounding=ROUND_DOWN))

notional = None
if order_type == "market":
    notional = None
elif order_type == "limit":
    notional = quantity * price if price else None
elif order_type == "stop-limit":
    notional = quantity * price if price else None

if notional is not None:
    st.markdown(f"""
        <div class="notional-display">
            <strong>💰 Order Value: {notional:,.2f} USDT</strong>
        </div>
    """, unsafe_allow_html=True)
    
    if notional < 100:
        st.markdown("""
            <div class="warning-card">
                ⚠ <strong>Warning:</strong> Order value is below minimum requirement of 100 USDT
            </div>
        """, unsafe_allow_html=True)

# Stop-limit validation
immediate_trigger = False
if order_type == "stop-limit" and price is not None and stop_price is not None:
    if side == "BUY" and stop_price <= price:
        immediate_trigger = True
    if side == "SELL" and stop_price >= price:
        immediate_trigger = True

if immediate_trigger:
    st.markdown("""
        <div class="warning-card">
            ⚠ <strong>Stop-Limit Configuration Issue:</strong><br>
            For BUY orders: Stop price should be above limit price<br>
            For SELL orders: Stop price should be below limit price
        </div>
    """, unsafe_allow_html=True)

# Helper functions
def clean_error_message(msg):
    if "APIError" in msg:
        parts = msg.split("): ")
        if len(parts) > 1:
            return parts[1].strip()
        return msg
    return msg

def format_order_result(result):
    if "error" in result:
        st.markdown(f"""
            <div class="error-card">
                <strong>❌ Order Failed:</strong><br>
                {clean_error_message(result['error'])}
            </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("""
        <div class="success-card">
            <strong>✅ Order Placed Successfully!</strong>
        </div>
    """, unsafe_allow_html=True)

    # Order summary table
    order_data = {
        "Order ID": result.get('orderId', 'N/A'),
        "Symbol": result.get('symbol', 'N/A'),
        "Side": result.get('side', 'N/A'),
        "Type": result.get('type', 'N/A'),
        "Status": result.get('status', 'N/A'),
        "Price": result.get('price', 'N/A'),
        "Quantity": result.get('origQty', 'N/A'),
        "Time in Force": result.get('timeInForce', 'N/A')
    }

    st.markdown('<div class="order-summary">', unsafe_allow_html=True)
    st.table(order_data)
    st.markdown('</div>', unsafe_allow_html=True)

# Add automatic time sync for Binance API timestamp errors
def sync_binance_time(client):
    try:
        # Get server time and set timestamp offset for the client
        server_time = client.futures_time()['serverTime']
        local_time = int(time.time() * 1000)
        client.timestamp_offset = server_time - local_time
    except Exception:
        client.timestamp_offset = 0

# Place Order Button
st.markdown('<div style="margin-top: 32px; text-align: center;">', unsafe_allow_html=True)

if st.button("🚀 Execute Trade", key="place_order_btn", use_container_width=True):
    api_key_clean = api_key.strip() if api_key else ""
    api_secret_clean = api_secret.strip() if api_secret else ""
    
    if not api_key_clean or not api_secret_clean:
        st.markdown("""
            <div class="error-card">
                <strong>❌ Authentication Required:</strong><br>
                Please enter your Binance Testnet API credentials to continue.
            </div>
        """, unsafe_allow_html=True)
    elif notional is not None and notional < 100:
        st.markdown("""
            <div class="error-card">
                <strong>❌ Order Value Too Low:</strong><br>
                Order notional value must be at least 100 USDT.
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🔄 Processing order..."):
            bot = BasicBot(api_key_clean, api_secret_clean, testnet=True)
            sync_binance_time(bot.client)
            # Adjust precision for BTCUSDT
            q = quantity
            p = price
            sp = stop_price
            if symbol.upper() == "BTCUSDT":
                q = adjust_precision(quantity, "0.001")
                if price is not None:
                    p = adjust_precision(price, "0.1")
                if stop_price is not None:
                    sp = adjust_precision(stop_price, "0.1")
            # Execute order
            if order_type == "market":
                result = bot.place_market_order(symbol, side, q)
            elif order_type == "limit":
                result = bot.place_limit_order(symbol, side, q, p)
            elif order_type == "stop-limit":
                result = bot.place_stop_limit_order(symbol, side, q, p, sp)
            else:
                result = {"error": "Unknown order type."}
            # If timestamp error, sync and retry with a short delay
            if "error" in result and "Timestamp for this request" in result["error"]:
                sync_binance_time(bot.client)
                time.sleep(1)  # Wait 1 second to ensure local clock is behind server
                if order_type == "market":
                    result = bot.place_market_order(symbol, side, q)
                elif order_type == "limit":
                    result = bot.place_limit_order(symbol, side, q, p)
                elif order_type == "stop-limit":
                    result = bot.place_stop_limit_order(symbol, side, q, p, sp)
            format_order_result(result)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # Close trading card
st.markdown("</div>", unsafe_allow_html=True)  # Close container

# Footer
st.markdown("""
    <div class="footer">
        <p style="margin: 0; font-size: 15px;">
            <strong>PrimeTrade Pro</strong> © 2025 | Powered by Binance Futures Testnet
        </p>
        <p style="margin: 8px 0 0 0; font-size: 13px; opacity: 0.8;">
            Professional trading interface for educational and testing purposes only
        </p>
    </div>
""", unsafe_allow_html=True)