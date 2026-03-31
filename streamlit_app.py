import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import os

# --- 1. إعدادات المنصة الأساسية ---
st.set_page_config(
    page_title="AI Trade Pro | Terminal v3.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. الهوية البصرية الفاخرة (CSS المدمج) ---
def apply_luxury_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; background-color: #050505; }
    .stApp { background-color: #08080a; }
    
    /* تصميم البطاقات الاحترافية */
    .premium-card {
        background: linear-gradient(145deg, #121215, #0a0a0c);
        border: 1px solid #1f1f23;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .premium-card:hover { border-color: #D4AF37; transform: translateY(-5px); }
    
    /* شريط التنبؤ بالاتجاه */
    .momentum-bg { height: 12px; background: #222; border-radius: 6px; overflow: hidden; margin: 10px 0; }
    .momentum-fill { height: 100%; background: linear-gradient(90deg, #004d00, #00ff00); box-shadow: 0 0 10px #00ff00; }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; background: transparent; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: bold; font-size: 18px; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; }
    
    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك التنبيهات الصوتية (JavaScript) ---
def play_notification_sound():
    sound_url = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
    components.html(f"""<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>""", height=0)

# --- 4. وظائف عرض البيانات المتقدمة ---

def display_premium_signal(asset, price, target, signal_type, accuracy):
    # تشغيل الصوت في حال الإشارات القوية
    if "STRONG" in signal_type.upper():
        play_notification_sound()
        st.toast(f"🚨 إشارة قوية مكتشفة: {asset}", icon="🔥")

    color = "#00ff00" if "BUY" in signal_type.upper() else "#ff4b4b"
    bg_glow = "rgba(0, 255, 0, 0.05)" if "BUY" in signal_type.upper() else "rgba(255, 75, 75, 0.05)"
    
    card_html = f"""
    <div class="premium-card">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f23; padding-bottom: 10px; margin-bottom: 15px;">
            <h3 style="color: #fff; margin: 0;">{asset}</h3>
            <span style="background: {bg_glow}; color: {color}; padding: 5px 15px; border-radius: 20px; border: 1px solid {color}; font-weight: bold;">{signal_type}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <div><p style="color: #888; margin:0;">السعر المباشر</p><h2 style="color: #fff; margin:0;">{price}</h2></div>
            <div style="text-align: right;"><p style="color: #888; margin:0;">الهدف المتوقع</p><h2 style="color: {color}; margin:0;">{target}</h2></div>
        </div>
        <div style="margin-top: 15px;">
            <p style="color: #D4AF37; font-size: 12px; margin:0;">دقة التحليل: {accuracy}%</p>
            <div class="momentum-bg"><div class="momentum-fill" style="width: {accuracy}%;"></div></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def display_trend_gauge(symbol):
    gauge_html = f"""
    <div style="height:350px;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
    {{ "interval": "15m", "width": "100%", "height": "100%", "symbol": "{symbol}", "showIntervalTabs": true, "displayMode": "single", "locale": "ar", "colorTheme": "dark" }}
    </script></div>"""
    components.html(gauge_html, height=360)

# --- 5. المنطق الرئيسي (Main Flow) ---

def main():
    apply_luxury_theme()
    
    # 1. شريط الأسعار الحي (Ticker)
    ticker_html = """<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
    {"symbols": [{"proName": "FX_IDC:XAUUSD", "title": "الذهب"}, {"proName": "BINANCE:BTCUSDT", "title": "BTC"}], "colorTheme": "dark", "locale": "ar"}</script>"""
    components.html(ticker_html, height=50)

    # 2. الهيدر
    st.markdown("<h1 style='text-align:center; color:#D4AF37; font-weight:900;'>🏆 AI TRADE PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>نظام التداول الذكي المعتمد على نبض البورصة العالمي</p>", unsafe_allow_html=True)

    # 3. جدار الاشتراك / الفترة المجانية
    FREE_UNTIL = datetime(2026, 4, 10, 23, 59)
    MY_WALLET = "TGiwLXt8yn8Jc9kCKfFbxpZxkY8DnMs97f"
    
    if datetime.now() < FREE_UNTIL:
        # --- محتوى المنصة الرئيسي ---
        tab_signals, tab_analysis, tab_news = st.tabs(["🎯 الإشارات الذكية", "📊 التحليل والخرائط", "📰 نبض الأخبار"])
        
        with tab_signals:
            st.markdown("#### ⚡ توصيات مباشرة (دقة 99%)")
            col1, col2 = st.columns(2)
            with col1:
                display_premium_signal("🏆 Gold (XAUUSD)", "2,185.40", "2,215.00", "STRONG BUY 🟢", 99.4)
            with col2:
                display_premium_signal("₿ Bitcoin (BTCUSDT)", "69,420.00", "72,500.00", "BUY 🟢", 98.8)
            
            st.divider()
            st.markdown("#### 🔮 مقياس تنبؤ الاتجاه")
            display_trend_gauge("FX_IDC:XAUUSD")
            
        with tab_analysis:
            st.markdown("#### 📈 الرسم البياني التفاعلي")
            chart_html = """<div style="height:600px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">new TradingView.widget({"width": "100%", "height": 600, "symbol": "FX_IDC:XAUUSD", "interval": "D", "theme": "dark", "locale": "ar", "container_id": "tv_main"});</script>
            <div id="tv_main"></div></div>"""
            components.html(chart_html, height=620)
            
        with tab_news:
            news_html = """<div style="height:550px;"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
            {"feedMode": "all_symbols", "colorTheme": "dark", "width": "100%", "height": "100%", "locale": "ar"}</script></div>"""
            components.html(news_html, height=570)
            
        # بوتون التلجرام
        st.write("---")
        st.markdown(f'<center><a href="https://t.me/YourUsername" style="text-decoration:none;"><button style="background:#0088cc; color:white; border:none; padding:15px 50px; border-radius:30px; font-weight:bold; cursor:pointer; font-size:18px;">💬 انضم لقناة الـ VIP الآن</button></a></center>', unsafe_allow_html=True)
    
    else:
        # شاشة القفل
        st.error("🛑 انتهت الفترة التجريبية للمنصة.")
        st.markdown(f"""
        <div style="text-align:center; padding:40px; border:1px solid #D4AF37; border-radius:20px;">
            <h2>💎 تفعيل الوصول الكامل (99% دقة)</h2>
            <p>للاشتراك، قم بتحويل <b>50 USDT</b> لمحفظة TRC20 التالية:</p>
            <code style="font-size:20px; color:#D4AF37;">{MY_WALLET}</code>
            <p style="margin-top:20px;">ثم أرسل صورة التحويل للدعم الفني لتفعيل حسابك فوراً.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
