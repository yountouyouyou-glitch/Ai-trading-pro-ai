import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# --- 1. إعدادات الأداء الفائق ---
st.set_page_config(
    page_title="AI Trade Pro | Global Terminal",
    page_icon="🏆",
    layout="wide"
)

# --- 2. الإعدادات الأساسية ---
MY_WALLET = "TGiwLXt8yn8Jc9kCKfFbxpZxkY8DnMs97f"
TELEGRAM_USER = "YourTelegramUsername"
FREE_UNTIL = datetime(2026, 4, 10, 23, 59)

# --- 3. محرك البيانات السريع (Caching) ---
@st.cache_data(ttl=60) # تحديث البيانات كل دقيقة لضمان الدقة والسرعة
def get_live_market_data():
    return [
        {"الأصل": "🏆 Gold (XAU)", "السعر": "2,185.20", "القوة": 94, "الحالة": "STRONG BUY 🟢", "الهدف": "$2,210"},
        {"الأصل": "BTC / USDT", "السعر": "69,420.50", "القوة": 91, "الحالة": "BUY 🟢", "الهدف": "$72,000"},
        {"الأصل": "ETH / USDT", "السعر": "3,510.15", "القوة": 88, "الحالة": "WAIT ⏳", "الهدف": "---"},
        {"الأصل": "SOL / USDT", "السعر": "185.50", "القوة": 85, "الحالة": "SELL 🔴", "الهدف": "$172.00"},
        {"الأصل": "BNB / USDT", "السعر": "590.30", "القوة": 84, "الحالة": "BUY 🟢", "الهدف": "$620.00"},
    ]

# --- 4. واجهة المستخدم الاحترافية ---

def display_header():
    if os.path.exists("logo.png"):
        st.image("logo.png", width=220)
    else:
        st.markdown("<h1 style='color: #D4AF37; text-align:center;'>🏆 AI TRADE PRO</h1>", unsafe_allow_html=True)
    st.write("---")

def display_signals_dashboard():
    st.markdown("### ⚡ إشارات التداول الذكية (دقة عالية)")
    data = get_live_market_data()
    
    # رأس القائمة
    h1, h2, h3, h4 = st.columns([1.5, 1, 1.5, 1])
    h1.write("**الأصل المالي**")
    h2.write("**السعر الحالي**")
    h3.write("**قوة الإشارة (AI)**")
    h4.write("**التوصية**")
    
    for item in data:
        with st.container():
            c1, c2, c3, c4 = st.columns([1.5, 1, 1.5, 1])
            with c1:
                st.markdown(f"**{item['الأصل']}**")
            with c2:
                st.markdown(f"`{item['السعر']}`")
            with c3:
                # عرض شريط تقدم ملون يوضح دقة الإشارة
                st.progress(item['القوة'] / 100)
                st.caption(f"دقة التحليل: {item['القوة']}%")
            with c4:
                color = "#00ff00" if "BUY" in item['الحالة'] else "#ff4b4b"
                if "WAIT" in item['الحالة']: color = "#ffd700"
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>{item['الحالة']}</span>", unsafe_allow_html=True)
            st.divider()

def display_news_section():
    st.markdown("### 📰 نبض الأسواق العاجل")
    news = [
        {"T": "10:30 AM", "N": "📣 الفيدرالي يثبت الفائدة، والذهب يتجه لاختراق مستويات تاريخية."},
        {"T": "09:15 AM", "N": "🚀 تدفقات مؤسساتية ضخمة للبيتكوين ترفع التوقعات لـ 75k."},
        {"T": "08:00 AM", "N": "⚠️ توترات جيوسياسية تزيد من بريق الذهب كملاذ آمن."}
    ]
    for n in news:
        st.info(f"**{n['T']}** | {n['N']}")

def display_contact_footer():
    st.write("---")
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #0e1117; border-radius: 15px; border: 1px solid #D4AF37;">
            <p>للمساعدة الفنية أو تفعيل الاشتراكات VIP</p>
            <a href="https://t.me/{TELEGRAM_USER}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #0088cc; color: white; padding: 10px 25px; border-radius: 20px; border: none; cursor: pointer; font-weight: bold;">
                    🚀 تواصل معنا عبر تلجرام
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# --- 5. منطق التحكم والوصول ---

def main():
    display_header()
    
    if 'auth' not in st.session_state:
        st.session_state['auth'] = False

    is_trial = datetime.now() < FREE_UNTIL

    if is_trial or st.session_state['auth']:
        # عرض حالة العرض المجاني
        if is_trial:
            time_left = FREE_UNTIL - datetime.now()
            st.success(f"🔓 فترة التجربة المجانية نشطة. متبقي: {time_left.days} يوم و {time_left.seconds//3600} ساعة.")
        
        # عرض المحتوى الأساسي
        display_signals_dashboard()
        display_news_section()
        display_contact_footer()
        
    else:
        # شاشة القفل (بعد 10 أبريل)
        st.error("🛑 انتهت الفترة المجانية (10 أيام).")
        st.markdown("### 💎 استمر في تلقي الإشارات الاحترافية")
        st.write("سعر الاشتراك: **50 USDT**")
        st.code(MY_WALLET, language="text")
        
        txid = st.text_input("أدخل رقم العملية (TXID) للتفعيل الفوري:")
        if st.button("تفعيل الحساب ✅"):
            if len(txid) > 15:
                st.session_state['auth'] = True
                st.success("تم التفعيل! جاري التحميل...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("رقم العملية غير صحيح.")
        
        display_contact_footer()

if __name__ == "__main__":
    main()
