import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="AI Trade Pro | Live Terminal", layout="wide")

# --- 2. دالة جلب إشارة السعر الحية (الربط المباشر مع TradingView) ---
def display_live_signal(symbol, title):
    st.markdown(f"### 🎯 إشارة {title} (تحديث لحظي)")
    # هذا الكود يجلب السعر والتحليل الفني مباشرة من البورصة
    tv_html = f"""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1m",
        "width": "100%",
        "isTransparent": false,
        "height": "420",
        "symbol": "{symbol}",
        "showIntervalTabs": true,
        "displayMode": "single",
        "locale": "ar",
        "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(tv_html, height=450)

# --- 3. الهيكل الرئيسي للموقع ---
def main():
    # شريط الأسعار العلوي (يتحرك دائماً)
    ticker_html = """<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
    {"symbols": [{"proName": "FOREXCOM:XAUUSD", "title": "الذهب"}, {"proName": "BINANCE:BTCUSDT", "title": "BTC"}], "colorTheme": "dark", "locale": "ar"}</script>"""
    components.html(ticker_html, height=50)

    # الشعار
    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>🏆 AI TRADE PRO</h1>", unsafe_allow_html=True)
    
    # التحقق من الفترة المجانية
    FREE_UNTIL = datetime(2026, 4, 10, 23, 59)
    if datetime.now() < FREE_UNTIL:
        st.success("🔓 وضع الوصول المباشر نشط - الأسعار محدثة من البورصة عالمياً")
        
        # توزيع الإشارات في أعمدة (الذهب والبيتكوين)
        col1, col2 = st.columns(2)
        
        with col1:
            # ربط حي بذهب فوركس (XAUUSD)
            display_live_signal("FX_IDC:XAUUSD", "الذهب العالمي")
            
        with col2:
            # ربط حي ببيتكوين منصة بينانس (BTCUSDT)
            display_live_signal("BINANCE:BTCUSDT", "البيتكوين")

        st.divider()
        
        # إضافة شارت تفاعلي للتأكيد البصري
        st.markdown("### 📈 الرسم البياني التفاعلي")
        chart_html = """
        <div style="height:500px;">
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({"width": "100%", "height": 500, "symbol": "FX_IDC:XAUUSD", "interval": "1", "theme": "dark", "locale": "ar", "container_id": "tv_chart"});
          </script>
          <div id="tv_chart"></div>
        </div>"""
        components.html(chart_html, height=520)

    else:
        st.error("🛑 انتهت الفترة المجانية. يرجى الاشتراك لتفعيل الربط الحي.")
        st.info("سعر الاشتراك 50 USDT لمده شهر.")

if __name__ == "__main__":
    main()
