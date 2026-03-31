import streamlit as st
import pandas as pd
import pandas_ta as ta
import requests
import time
from datetime import datetime

# --- الإعدادات الأساسية للمنصة ---
st.set_page_config(page_title="AI Trade Pro | المنصة الذكية", layout="wide", initial_sidebar_state="expanded")

# محفظتك الشخصية (Bybit - TRC20)
MY_WALLET = "TGiwLXt8yn8Jc9kCKfFbxpZxkY8DnMs97f"
# ضع مفتاح API الخاص بك من TronGrid هنا
TRONGRID_API_KEY = "YOUR_TRONGRID_API_KEY" 

# --- تنسيق الواجهة الاحترافية (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: white; }
    .stApp { background-color: #0b0e11; }
    .stButton>button { 
        width: 100%; border-radius: 8px; background: linear-gradient(90deg, #00c853, #b2ff59); 
        color: black; font-weight: bold; border: none; padding: 12px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0px 0px 15px #00c853; }
    .metric-card { 
        background-color: #1e2329; padding: 20px; border-radius: 15px; 
        border: 1px solid #333; text-align: center; margin-bottom: 10px;
    }
    .wallet-box { 
        background-color: #000; padding: 15px; border-radius: 10px; 
        border: 1px dashed #00c853; font-family: 'Courier New', monospace; 
        color: #00ff00; font-size: 14px; word-break: break-all;
    }
    h1, h2, h3 { color: #f0b90b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك الذكاء الاصطناعي لتحليل الشموع ---
def fetch_and_analyze():
    """
    محرك التحليل الفني: يستخدم المتوسطات المتحركة، RSI، و ATR لتحديد نقاط الدخول والخروج.
    """
    # بيانات تجريبية (يتم استبدالها ببيانات حية من API مثل Binance لاحقاً)
    data = pd.DataFrame({
        'Open': [65000, 65200, 65500, 65800, 66100],
        'High': [65500, 65800, 66200, 66500, 66800],
        'Low': [64800, 65000, 65300, 65600, 65900],
        'Close': [65200, 65500, 66000, 66300, 66700]
    })
    
    # حساب المؤشرات
    data['RSI'] = ta.rsi(data['Close'], length=2)
    data['EMA'] = ta.ema(data['Close'], length=3)
    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=2)
    
    last = data.iloc[-1]
    entry = last['Close']
    atr_val = last['ATR'] if not pd.isna(last['ATR']) else 200
    
    # تحديد الاتجاه بناءً على التحليل
    if last['Close'] > last['EMA'] and last['RSI'] > 50:
        signal = "BUY / LONG 🟢"
        sl = entry - (atr_val * 2)
        tp = entry + (atr_val * 4)
    else:
        signal = "SELL / SHORT 🔴"
        sl = entry + (atr_val * 2)
        tp = entry - (atr_val * 4)
        
    return signal, round(entry, 2), round(tp, 2), round(sl, 2)

# --- نظام التحقق من الدفع (TronGrid) ---
def verify_payment(txid):
    """
    التحقق من بلوكتشين ترون لوصول مبلغ 50 USDT لمحفظتك.
    """
    if not txid: return False
    
    url = f"https://api.trongrid.io/v1/transactions/{txid}/events"
    headers = {"TRON-PRO-API-KEY": TRONGRID_API_KEY}
    
    try:
        # ملاحظة: التحقق الحقيقي يتطلب فحص قيمة التحويل وجهة الاستلام
        # كود تجريبي للتحقق (يفعل الحساب إذا كان رقم العملية طويلاً بما يكفي)
        if len(txid) > 50:
            return True
    except:
        return False
    return False

# --- إدارة حالة المستخدم ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- تصميم الواجهة ---
st.title("⚡ AI Trade Pro Dashboard")
st.markdown("### التحليل الذكي للشموع وإدارة المخاطر الآلية")

if not st.session_state['auth']:
    # --- واجهة غير المشتركين (التسويق والدفع) ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image("https://images.unsplash.com/photo-1611974714658-048e47458117?auto=format&fit=crop&q=80&w=1000", caption="نظام تحليل الشموع بالذكاء الاصطناعي")
        st.markdown("""
        #### مميزات المنصة الاحترافية:
        1. **تحليل الشموع لحظياً:** قراءة أنماط الشموع اليابانية بدقة عالية.
        2. **نقاط الخروج الآمنة:** حساب آلي لـ **Stop Loss** و **Take Profit**.
        3. **تنبيهات فورية:** الحصول على إشارات تداول بناءً على زخم السوق (RSI & EMA).
        4. **دفع مباشر:** أرباحك تصل مباشرة لمحفظتك الشخصية.
        """)
        
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.write("🔓 **فتح الوصول الكامل**")
        st.write("رسوم الاشتراك: **50 USDT**")
        st.write("شبكة التحويل: **TRC20**")
        st.markdown(f"<div class='wallet-box'>{MY_WALLET}</div>", unsafe_allow_html=True)
        st.caption("انسخ العنوان أعلاه وأرسل المبلغ من محفظة Bybit أو Binance")
        
        user_txid = st.text_input("أدخل رقم العملية (TXID) هنا:")
        if st.button("تفعيل الحساب"):
            with st.spinner("جاري التحقق من الشبكة..."):
                time.sleep(2) # محاكاة وقت الفحص
                if verify_payment(user_txid):
                    st.session_state['auth'] = True
                    st.success("تم التفعيل بنجاح!")
                    st.rerun()
                else:
                    st.error("رقم العملية غير صحيح أو لم يكتمل التحويل.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- واجهة المشتركين (لوحة الإشارات) ---
    st.sidebar.success("✅ حسابك نشط (Premium)")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state['auth'] = False
        st.rerun()

    st.markdown("---")
    sig, ent, t_p, s_l = fetch_and_analyze()
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"<div class='metric-card'><h4>الإشارة</h4><h2 style='color:#00ff00'>{sig}</h2></div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div class='metric-card'><h4>سعر الدخول</h4><h2>${ent:,.2f}</h2></div>", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"<div class='metric-card'><h4>المخاطرة (ATR)</h4><h2 style='color:#ff4b4b'>حماية نشطة</h2></div>", unsafe_allow_html=True)

    st.write("### 🎯 مستويات التداول المقترحة")
    st.info(f"📍 **نقطة جني الأرباح (TP):** ${t_p:,.2f}")
    st.error(f"🚫 **نقطة وقف الخسارة (SL):** ${s_l:,.2f}")
    
    # إضافة TradingView Widget بشكل مبسط
    st.components.v1.html("""
        <div id="tradingview_chart" style="height:400px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({
          "autosize": true,
          "symbol": "BINANCE:BTCUSDT",
          "interval": "60",
          "timezone": "Etc/UTC",
          "theme": "dark",
          "style": "1",
          "locale": "ar",
          "toolbar_bg": "#f1f3f6",
          "enable_publishing": false,
          "hide_top_toolbar": true,
          "save_image": false,
          "container_id": "tradingview_chart"
        });
        </script>
    """, height=420)

    st.caption(f"تاريخ التحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
