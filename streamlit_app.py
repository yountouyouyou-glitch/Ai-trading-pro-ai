import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# --- 1. الإعدادات الأساسية ---
st.set_page_config(page_title="AI Trade Pro | Absolute Accuracy", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=30 * 1000, key="global_final_pulse")

# --- 2. الهوية البصرية (تصميم الدرع والتأكيدات) ---
def apply_pro_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    
    .status-card {
        background: linear-gradient(145deg, #111115, #050505);
        border: 1px solid #2a2a35; border-radius: 20px; padding: 30px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .verify-badge {
        display: inline-block; padding: 2px 8px; border-radius: 4px;
        font-size: 11px; margin-bottom: 5px; border: 1px solid #444; color: #888;
    }
    .signal-box {
        width: 100%; text-align: center; padding: 20px; border-radius: 12px;
        font-size: 22px; font-weight: 900; margin-top: 20px; text-transform: uppercase;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك التحليل الفني الصارم (Strict Logic) ---
def get_advanced_analysis(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="5d", interval="1m")
        if df.empty or len(df) < 30: return None

        # حساب المؤشرات الفنية
        df['EMA'] = df['Close'].ewm(span=20, adjust=False).mean()
        # RSI بسيط
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))

        curr = df.iloc[-1]
        prev = df.iloc[-2]
        
        price = round(curr['Close'], 2)
        rsi = curr['RSI']
        ema = curr['EMA']
        
        # تحليل الشموع (Candlestick Analysis)
        is_green = curr['Close'] > curr['Open']
        is_red = curr['Close'] < curr['Open']
        
        # شروط الشراء المؤكد (السعر فوق EMA + RSI صاعد + شمعة خضراء)
        buy_cond = (price > ema) and (rsi > 50) and is_green
        # شروط البيع المؤكد (السعر تحت EMA + RSI هابط + شمعة حمراء)
        sell_cond = (price < ema) and (rsi < 50) and is_red

        if buy_cond:
            return price, round(price * 1.007, 2), "شراء مؤكد 🟢", "#00ff00", ["RSI صاعد ✅", "EMA دعم ✅", "شمعة شرائية ✅"]
        elif sell_cond:
            return price, round(price * 0.993, 2), "بيع مؤكد 🔴", "#ff4b4b", ["RSI هابط ✅", "EMA مقاومة ✅", "شمعة بيعية ✅"]
        else:
            return price, price, "انتظار (تذبذب) ⏳", "#aaaaaa", ["جاري تحليل الموجة...", "انتظر تطابق المؤشرات"]
    except: return None

# --- 4. الهيكل التنفيذي للموقع ---
def main():
    apply_pro_style()
    
    # شريط الأسعار من TradingView
    components.html('<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>{"symbols": [{"proName": "FX_IDC:XAUUSD", "title": "Gold"}, {"proName": "BINANCE:BTCUSDT", "title": "BTC"}], "colorTheme": "dark", "locale": "ar"}</script>', height=50)

    st.markdown("<h1 style='text-align:center; color:#D4AF37; font-weight:900;'>💎 AI TRADE PRO: SUPREME ENGINE</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#555;'>نظام تحليل الشموع اليابانية والمؤشرات | {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    assets = [("الذهب (Gold/USD)", "GC=F"), ("بيتكوين (BTC/USDT)", "BTC-USD")]
    slots = [col1, col2]

    for i, (name, sym) in enumerate(assets):
        data = get_advanced_analysis(sym)
        if data:
            price, target, signal, color, checks = data
            with slots[i]:
                # عرض البطاقة بالتصميم الذي طلبته
                st.markdown(f"""
                <div class="status-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:20px; font-weight:bold; color:#D4AF37;">{name}</span>
                        <div style="text-align:right;">
                            {''.join([f'<div class="verify-badge">{c}</div>' for c in checks])}
                        </div>
                    </div>
                    
                    <div style="margin-top:20px;">
                        <small style="color:#666;">السعر المباشر (LIVE)</small>
                        <h1 style="margin:0; font-size:50px;">${price:,}</h1>
                    </div>
                    
                    <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <small style="color:#666;">الهدف الفني المتوقع</small>
                            <h3 style="margin:0; color:{color};">${target:,}</h3>
                        </div>
                        <div style="width:50%; height:4px; background:#222; border-radius:2px;">
                            <div style="width:100%; height:100%; background:{color}; box-shadow:0 0 10px {color};"></div>
                        </div>
                    </div>
                    
                    <div class="signal-box" style="background:{color}15; border:1px solid {color}; color:{color};">
                        {signal}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # دمج أدوات TradingView الرسمية في الأسفل
    st.markdown("### 📊 مركز التحليل والخرائط الحية")
    c_left, c_right = st.columns([1, 2])
    
    with c_left:
        # عداد القوة الفنية من TradingView
        components.html("""<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>{
            "interval": "1m", "width": "100%", "height": 450, "symbol": "FX_IDC:XAUUSD", "showIntervalTabs": true, "displayMode": "single", "locale": "ar", "colorTheme": "dark"
        }</script>""", height=460)

    with c_right:
        # الشارت التفاعلي
        components.html("""<div style="height:450px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">new TradingView.widget({"width": "100%", "height": 450, "symbol": "FX_IDC:XAUUSD", "interval": "1", "theme": "dark", "locale": "ar", "container_id": "tv_chart"});</script>
        <div id="tv_chart"></div></div>""", height=460)

if __name__ == "__main__":
    main()
