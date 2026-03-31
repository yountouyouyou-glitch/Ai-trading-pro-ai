import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf # المكتبة الأساسية لجلب الأسعار
from datetime import datetime

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="AI Trade Pro | Live", layout="wide")

def apply_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; background-color: #08080a; color: white; }
    .stApp { background-color: #08080a; }
    .premium-card {
        background: linear-gradient(145deg, #121215, #0a0a0c);
        border: 1px solid #1f1f23;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .signal-tag { padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك جلب البيانات والتحليل الذكي ---
def get_market_data(ticker_symbol):
    try:
        # جلب بيانات السعر من Yahoo Finance
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="1d", interval="1m")
        if df.empty: return None
        
        current_price = round(df['Close'].iloc[-1], 2)
        prev_close = ticker.info.get('previousClose', current_price)
        
        # حساب السعر المتوقع (الهدف) برمجياً ليكون منطقياً
        # إذا كان الاتجاه صاعد، الهدف = السعر الحالي + 0.5%
        # إذا كان الاتجاه هابط، الهدف = السعر الحالي - 0.5%
        change = current_price - prev_close
        if change > 0:
            signal = "STRONG BUY 🟢"
            target = round(current_price * 1.006, 2) # هدف صعودي
            color = "#00ff00"
        else:
            signal = "STRONG SELL 🔴"
            target = round(current_price * 0.994, 2) # هدف هبوطي
            color = "#ff4b4b"
            
        return current_price, target, signal, color
    except:
        return None

# --- 3. وظيفة عرض البطاقات الديناميكية ---
def render_signal_card(asset_name, ticker_symbol):
    data = get_market_data(ticker_symbol)
    if not data:
        st.error(f"خطأ في جلب بيانات {asset_name}")
        return

    price, target, signal, color = data
    
    st.markdown(f"""
    <div class="premium-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin:0;">{asset_name}</h3>
            <span class="signal-tag" style="border: 1px solid {color}; color: {color};">{signal}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <p style="color: #888; font-size: 14px; margin:0;">السعر المباشر</p>
                <h2 style="margin:0;">${price:,}</h2>
            </div>
            <div style="text-align: right;">
                <p style="color: #888; font-size: 14px; margin:0;">السعر المتوقع (AI Target)</p>
                <h2 style="margin:0; color: {color};">${target:,}</h2>
            </div>
        </div>
        <div style="margin-top: 15px; height: 4px; background: #222; border-radius: 2px;">
            <div style="width: 99%; background: {color}; height: 100%; box-shadow: 0 0 10px {color};"></div>
        </div>
        <p style="font-size: 11px; color: #D4AF37; margin-top: 8px;">🕒 تم التحديث التلقائي: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. واجهة المستخدم الرئيسية ---
def main():
    apply_style()
    
    # شريط الأسعار التفاعلي
    ticker_html = '<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>{"symbols": [{"proName": "FX_IDC:XAUUSD", "title": "Gold"}, {"proName": "BINANCE:BTCUSDT", "title": "BTC"}], "colorTheme": "dark", "locale": "ar"}</script>'
    components.html(ticker_html, height=50)

    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>🏆 AI TRADE PRO V3</h1>", unsafe_allow_html=True)

    # الأزرار والتحكم
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("🔄 تحديث الأسعار الآن"):
            st.rerun()

    # عرض الإشارات الحية
    c1, c2 = st.columns(2)
    with c1:
        render_signal_card("الذهب (XAU/USD)", "GC=F")
    with c2:
        render_signal_card("بيتكوين (BTC/USD)", "BTC-USD")

    # إضافة الشارت للتأكيد
    st.divider()
    chart_html = """<div style="height:500px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({"width": "100%", "height": 500, "symbol": "FX_IDC:XAUUSD", "interval": "1", "theme": "dark", "locale": "ar", "container_id": "tv_chart"});</script><div id="tv_chart"></div></div>"""
    components.html(chart_html, height=520)

if __name__ == "__main__":
    main()
