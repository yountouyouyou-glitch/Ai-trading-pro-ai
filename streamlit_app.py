import streamlit as st
import streamlit.components.v1 as components # لاستدعاء مصغرات TradingView
from datetime import datetime
import os
import time

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(
    page_title="AI Trade Pro | الذهب والعملات",
    page_icon="🏆",
    layout="wide"
)

# --- 2. الإعدادات العامة (تعديل يدوي) ---
MY_WALLET = "TGiwLXt8yn8Jc9kCKfFbxpZxkY8DnMs97f" # محفظة USDT TRC20
TELEGRAM_USER = "YourTelegramUsername"          # اسم مستخدم التلجرام الخاص بك
FREE_UNTIL = datetime(2026, 4, 10, 23, 59)      # نهاية الفترة المجانية

# --- 3. بيانات السوق وتوصيات الذكاء الاصطناعي (تعديل يدوي للحالة والدخول) ---
# ملاحظة: TradingView سيتكفل بعرض السعر الحي تلقائياً في الجدول والشارت
market_signals = [
    {"الأصل": "🏆 Gold (XAUUSD)", "الحالة": "STRONG BUY 🟢", "الدخول": "$2,185.20", "الهدف": "$2,210.00", "النجاح": "94%"},
    {"الأصل": "BTC / USDT", "الحالة": "BUY 🟢", "الدخول": "$69,420", "الهدف": "$72,000", "النجاح": "91%"},
    {"الأصل": "ETH / USDT", "الحالة": "WAIT ⏳", "الدخول": "مراقبة", "الهدف": "---", "النجاح": "88%"},
    {"الأصل": "SOL / USDT", "الحالة": "SELL 🔴", "الدخول": "$185.50", "الهدف": "$172.00", "النجاح": "85%"},
]

# --- 4. وظائف TradingView (للأسعار الحية والشارت) ---

def display_tv_ticker():
    # شريط أسعار متحرك في أعلى الصفحة
    ticker_html = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {
      "symbols": [
        {"proName": "FOREXCOM:XAUUSD", "title": "الذهب"},
        {"proName": "BINANCE:BTCUSDT", "title": "BTC"},
        {"proName": "BINANCE:ETHUSDT", "title": "ETH"},
        {"proName": "BINANCE:SOLUSDT", "title": "SOL"}
      ],
      "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": false, "displayMode": "adaptive", "locale": "ar"
    }
      </script>
    </div>
    """
    components.html(ticker_html, height=50)

def display_tv_market_overview():
    # جدول أسعار حي تفاعلي
    market_html = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>
      {
      "colorTheme": "dark", "dateRange": "12M", "showChart": false, "locale": "ar", "isTransparent": false, "showSymbolLogo": true,
      "width": "100%", "height": "350",
      "tabs": [
        {
          "title": "الأسعار الحية",
          "symbols": [
            {"s": "FOREXCOM:XAUUSD", "d": "Gold (XAU/USD)"},
            {"s": "BINANCE:BTCUSDT", "d": "Bitcoin"},
            {"s": "BINANCE:ETHUSDT", "d": "Ethereum"},
            {"s": "BINANCE:SOLUSDT", "d": "Solana"}
          ]
        }
      ]
    }
      </script>
    </div>
    """
    components.html(market_html, height=380)

def display_gold_chart():
    # شارت الذهب تفاعلي مع أدوات الرسم
    st.markdown("### 🏆 تحليلات الذهب الفنية (XAU/USD Chart)")
    chart_html = """
    <div class="tradingview-widget-container">
      <div id="tradingview_gold_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
      "width": "100%",
      "height": "550",
      "symbol": "FOREXCOM:XAUUSD",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "ar",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_gold_chart"
    }
      );
      </script>
    </div>
    """
    components.html(chart_html, height=570)

# --- 5. بقية الأقسام (الهوية، الأخبار، التلجرام، الاشتراك) ---

def display_header():
    if os.path.exists("logo.png"):
        st.image("logo.png", width=220)
    else:
        st.markdown("<h1 style='color: #D4AF37; text-align:center;'>🏆 AI TRADE PRO</h1>", unsafe_allow_html=True)
    st.write("---")

def display_ai_recommendations():
    # عرض توصيات الذكاء الاصطناعي (الحالة والنجاح)
    st.markdown("### 🎯 توصيات الذكاء الاصطناعي الحالية")
    for sig in market_signals:
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 1.5, 1, 1])
            with col1: st.write(f"**{sig['الأصل']}**")
            with col2: st.markdown(f"<span style='color: #00ff00; font-weight:bold;'>{sig['الحالة']}</span>", unsafe_allow_html=True)
            with col3: st.code(f"{sig['الدخول']}")
            with col4: st.metric("دقة الإشارة", sig['النجاح'])
            st.divider()

def display_news():
    st.markdown("### 📰 نبض السوق والأخبار العاجلة")
    news_items = [{"T": "10:30 AM", "N": "📣 الفيدرالي يلمح لتثبيت الفائدة والذهب يقفز لقمة جديدة."}]
    for n in news_items:
        st.info(f"**{n['T']}** | {n['N']}")

def display_contact():
    st.write("---")
    st.markdown(f"""
        <div style="text-align: center; padding: 25px; background-color: #111; border-radius: 15px; border: 1px dashed #ffd700;">
            <p style="color: #ccc;">هل لديك استفسار؟ تواصل مع الدعم الفني مباشرة</p>
            <a href="https://t.me/{TELEGRAM_USER}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #0088cc; color: white; padding: 10px 30px; border-radius: 20px; border: none; font-size: 16px; cursor: pointer; font-weight: bold;">
                    💬 تواصل معنا عبر Telegram
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# --- 6. المنطق الرئيسي للتشغيل ---

def main():
    display_tv_ticker() # عرض شريط الأسعار الحي
    display_header()
    
    if 'auth' not in st.session_state: st.session_state['auth'] = False
    is_free = datetime.now() < FREE_UNTIL

    if is_free or st.session_state['auth']:
        # عرض الوصول المجاني
        if is_free:
            time_left = FREE_UNTIL - datetime.now()
            st.success(f"🎁 وضع التجربة المجانية نشط (متصل بـ TradingView Live). متبقي {time_left.days} أيام.")
        
        # عرض جدول الأسعار الحية
        display_tv_market_overview()
        
        st.write("---")
        
        # عرض شارت الذهب التفاعلي (XAU/USD Chart)
        display_gold_chart()
        
        st.write("---")
        
        # عرض التوصيات (الدخول والأهداف)
        display_ai_recommendations()
        
        st.divider()
        display_news()
        display_contact()
        
    else:
        # شاشة القفل والاشتراك
        st.error("🛑 انتهت الفترة المجانية.")
        st.markdown("### 💎 باقة الاحتراف الشاملة (ذهب + عملات)")
        st.write("السعر: **50 USDT** | المحفظة:")
        st.code(MY_WALLET, language="text")
        
        txid = st.text_input("أدخل رقم العملية (TXID) للتفعيل الفوري:")
        if st.button("تفعيل الآن ✅"):
            if len(txid) > 15:
                st.session_state['auth'] = True
                st.success("تم التفعيل!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("رقم العملية غير صحيح.")
        
        display_contact()

if __name__ == "__main__":
    main()
