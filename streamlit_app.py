import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# --- 1. الإعدادات ونبض التحديث (30 ثانية) ---
st.set_page_config(page_title="AI Trade Pro | Extreme Accuracy", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=30 * 1000, key="final_unified_pulse")

# --- 2. محرك التصميم (CSS) - يمنع ظهور الأكواد كنصوص ---
def apply_unified_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    
    /* تصميم بطاقة الدرع */
    .shield-card {
        background: linear-gradient(145deg, #0f0f12, #050505);
        border: 1px solid #1f1f23; border-radius: 20px; padding: 30px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8); border-right: 5px solid #D4AF37;
    }
    .verify-tag {
        display: inline-block; padding: 2px 10px; border-radius: 5px;
        font-size: 11px; margin-bottom: 5px; border: 1px solid #333; color: #00ff00; background: rgba(0,255,0,0.05);
    }
    .signal-banner {
        width: 100%; text-align: center; padding: 20px; border-radius: 12px;
        font-size: 24px; font-weight: 900; margin-top: 20px;
    }
    /* إخفاء القوائم غير الضرورية */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك تحليل الشموع والمؤشرات (بدون أخطاء جلب) ---
def get_verified_analysis(symbol):
    try:
        # استخدام yf.download لضمان ثبات جلب البيانات
        df = yf.download(symbol, period="5d", interval="1m", progress=False)
        if df.empty or len(df) < 50: return None

        # حساب المؤشرات (EMA & RSI)
        ema_20 = df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = (100 - (100 / (1 + (gain / loss)))).iloc[-1]

        curr_p = round(df['Close'].iloc[-1], 2)
        is_green = df['Close'].iloc[-1] > df['Open'].iloc[-1]
        
        # منطق "شراء مؤكد" أو "بيع مؤكد"
        if curr_p > ema_20 and rsi > 50 and is_green:
            return curr_p, round(curr_p * 1.008, 2), "شراء مؤكد 🟢", "#00ff00", ["RSI صاعد ✅", "EMA دعم ✅", "شموع خضراء ✅"]
        elif curr_p < ema_20 and rsi < 50 and not is_green:
            return curr_p, round(curr_p * 0.992, 2), "بيع مؤكد 🔴", "#ff4b4b", ["RSI هابط ✅", "EMA مقاومة ✅", "شموع حمراء ✅"]
        else:
            return curr_p, curr_p, "انتظار (تذبذب) ⏳", "#aaaaaa", ["جاري الفلترة...", "انتظر تطابق المؤشرات"]
    except:
        return None

# --- 4. الهيكل الرئيسي للمنصة ---
def main():
    apply_unified_style()
    
    # شريط TradingView العلوي
    components.html('<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>{"symbols": [{"proName": "FX_IDC:XAUUSD", "title": "Gold"}, {"proName": "BINANCE:BTCUSDT", "title": "BTC"}], "colorTheme": "dark", "locale": "ar"}</script>', height=50)

    st.markdown("<h1 style='text-align:center; color:#D4AF37; font-weight:900;'>🏆 AI TRADE PRO TERMINAL</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#666;'>آخر تحديث للنظام: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    assets = [("الذهب (XAU/USD)", "GC=F"), ("بيتكوين (BTC/USD)", "BTC-USD")]
    slots = [col1, col2]

    for i, (name, sym) in enumerate(assets):
        data = get_verified_analysis(sym)
        with slots[i]:
            if data:
                price, target, signal, color, checks = data
                st.markdown(f"""
                <div class="shield-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <span style="font-size:22px; font-weight:bold;">{name}</span>
                        <div style="text-align:right;">{''.join([f'<div class="verify-tag">{c}</div><br>' for c in checks])}</div>
                    </div>
                    <div style="margin-top:20px;">
                        <small style="color:#888;">السعر المباشر</small>
                        <h1 style="margin:0; font-size:55px;">${price:,}</h1>
                    </div>
                    <div style="margin-top:15px; display:flex; justify-content:space-between;">
                        <div><small style="color:#888;">الهدف (Target)</small><h3 style="margin:0; color:{color};">${target:,}</h3></div>
                        <div style="width:40%; background:#222; height:4px; margin-top:25px; border-radius:2px;"><div style="width:100%; height:100%; background:{color};"></div></div>
                    </div>
                    <div class="signal-banner" style="background:{color}15; border:1px solid {color}; color:{color};">
                        {signal}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"⚠️ خطأ في مزامنة بيانات {name}")

    st.divider()

    # قسم الشارت الفني المباشر
    st.markdown("### 📊 التحليل الفني المتقدم (TradingView)")
    chart_code = """<div style="height:500px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">new TradingView.widget({"width": "100%", "height": 500, "symbol": "FX_IDC:XAUUSD", "interval": "1", "theme": "dark", "locale": "ar", "container_id": "tv_chart"});</script>
    <div id="tv_chart"></div></div>"""
    components.html(chart_code, height=520)

if __name__ == "__main__":
    main()
