import streamlit as st
from basic_bot import BasicBot
from decimal import Decimal, ROUND_DOWN
from binance.client import Client
from binance.exceptions import BinanceAPIException

st.set_page_config(
    page_title="PrimeTrade Pro - Binance Futures Trading", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS with modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .block-container {
        padding: 0 !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px 20px;
        margin: 0;
        color: white;
        text-align: center;
        box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    }
    
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 28px 24px;
        font-family: 'Inter', sans-serif;
    }
    
    .trading-card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid #e8ecf0;
        margin-bottom: 24px;
        max-width: 100%;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a202c;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
        background: none !important;
        padding: 0 !important;
    }
    
    .price-display {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 16px 0;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 2px 12px rgba(72, 187, 120, 0.3);
    }
    
    .info-box {
        background: #f7fafc;
        border-left: 4px solid #4299e1;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
        color: #2d3748;
    }
    
    .notional-display {
        background: #edf2f7;
        padding: 16px;
        border-radius: 8px;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        color: #2d3748;
        margin: 16px 0;
    }
    
    .input-group {
        margin-bottom: 20px;
    }
    
    .input-label {
        font-size: 14px;
        font-weight: 500;
        color: #4a5568;
        margin-bottom: 8px;
        display: block;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        font-size: 14px !important;
        max-width: 100% !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        max-width: 100% !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .success-card {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #22543d !important;
    }
    
    .success-card strong {
        color: #22543d !important;
    }
    
    .error-card {
        background: #fed7d7;
        border: 1px solid #feb2b2;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #742a2a !important;
    }
    
    .error-card strong {
        color: #742a2a !important;
    }
    
    .warning-card {
        background: #fffbeb;
        border: 1px solid #fbd38d;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #744210 !important;
    }
    
    .warning-card strong {
        color: #744210 !important;
    }
    
    .order-summary {
        background: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    }
    
    .order-summary table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .order-summary th,
    .order-summary td {
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .order-summary th {
        background: #edf2f7;
        font-weight: 600;
        color: #2d3748;
    }
    
    .footer {
        background: #2d3748;
        color: #a0aec0;
        text-align: center;
        padding: 20px;
        margin-top: 32px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        border-radius: 12px;
    }
    
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 28px; font-weight: 700;">⚡ PrimeTrade Pro</h1>
        <p style="margin: 8px 0 0 0; font-size: 15px; opacity: 0.9;">Professional Binance Futures Trading Platform</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="container">', unsafe_allow_html=True)

# API Credentials Card
st.markdown("""
    <div class="trading-card">
        <div class="card-header">
            <h2 class="card-title">🔐 API Configuration</h2>
        </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="info-box">
        <strong>🛡️ Security Notice:</strong> This interface connects to Binance Futures <strong>Testnet</strong> only. 
        Your API credentials are processed securely and never stored.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    api_key = st.text_input("🔑 API Key", type="password", placeholder="Enter your Binance Testnet API Key")
with col2:
    api_secret = st.text_input("🔒 API Secret", type="password", placeholder="Enter your Binance Testnet API Secret")

st.markdown("</div>", unsafe_allow_html=True)

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
                ⚠️ <strong>Warning:</strong> Order value is below minimum requirement of 100 USDT
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
            ⚠️ <strong>Stop-Limit Configuration Issue:</strong><br>
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
            
            format_order_result(result)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # Close trading card
st.markdown("</div>", unsafe_allow_html=True)  # Close container

# Footer
st.markdown("""
    <div class="footer">
        <p style="margin: 0; font-size: 14px;">
            <strong>PrimeTrade Pro</strong> © 2025 | Powered by Binance Futures Testnet
        </p>
        <p style="margin: 8px 0 0 0; font-size: 12px; opacity: 0.7;">
            Professional trading interface for educational and testing purposes only
        </p>
    </div>
""", unsafe_allow_html=True)