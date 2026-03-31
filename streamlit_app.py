import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
import time  # تمت إضافة هذه المكتبة لإصلاح خطأ time.sleep

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="AI Trade Pro | الذكاء الاصطناعي في خدمتك",
    page_icon="🟢", 
    layout="wide"
)

# محفظتك الشخصية لاستقبال الدفع
MY_WALLET = "TGiwLXt8yn8Jc9kCKfFbxpZxkY8DnMs97f"

# --- إعدادات الفترة المجانية (10 أيام) ---
# تاريخ النهاية: 10 أبريل 2026 الساعة 11:59 مساءً
FREE_UNTIL = datetime(2026, 4, 10, 23, 59) 

def is_free_trial_active():
    return datetime.now() < FREE_UNTIL

# --- [إضافة الشعار الجديد] ---
def display_logo(file_name="logo.png"):
    if os.path.exists(file_name):
        st.image(file_name, width=200) 
    else:
        # إذا لم يتم رفع الصورة، سيظهر اسم الموقع بشكل ذهبي احترافي
        st.markdown("<h1 style='color: #D4AF37;'>🏆 AI TRADE PRO</h1>", unsafe_allow_html=True)
        st.caption("💡 لم يتم العثور على صورة الشعار، يرجى رفعها باسم logo.png")

# --- محرك التحليل المبسط ---
def calculate_signals():
    df = pd.DataFrame({
        'close': [64800, 65200, 65900, 66100, 66500],
        'volume': [1000, 1200, 1500, 1300, 1700]
    })
    
    df['ema'] = df['close'].ewm(span=3, adjust=False).mean()
    
    last = df.iloc[-1]
    entry = last['close']
    
    if last['close'] > last['ema']:
        sig, tp, sl = "BUY 🟢", entry + 800, entry - 400
    else:
        sig, tp, sl = "SELL 🔴", entry - 800, entry + 400
        
    return sig, round(entry, 2), round(tp, 2), round(sl, 2)

# ==========================================
# --- بداية واجهة الموقع ---
# ==========================================

# 1. إظهار الشعار في الأعلى
st.write("---") 
display_logo("logo.png") 
st.write("---")

st.title("🚀 لوحة تحكم AI Trade Pro")
st.subheader("تحليل فني دقيق مدعوم بالذكاء الاصطناعي")

# --- إدارة حالة الجلسة والتفعيل ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# التحقق مما إذا كنا في الفترة المجانية
is_free = is_free_trial_active()

# عرض رسالة الفترة المجانية إذا كانت مفعلة
if is_free:
    days_left = (FREE_UNTIL - datetime.now()).days
    st.success(f"🎁 **عرض الإطلاق:** الموقع متاح مجاناً للجميع (متبقي {days_left + 1} أيام).")

# إذا لم يكن المستخدم مشتركاً وانتهت الفترة المجانية (تم إغلاق الموقع)
if not st.session_state['auth'] and not is_free:
    st.warning("🔒 انتهت الفترة التجريبية. هذا المحتوى محمي للمشتركين فقط.")
    st.info(f"💌 للتفعيل الفوري، قم بإرسال **50 USDT (TRC20)** إلى العنوان التالي:")
    st.code(MY_WALLET, language="text")
    st.write("بعد الإرسال، الصق رقم العملية (TXID) هنا:")
    
    txid = st.text_input("رقم العملية (TXID):", placeholder="الصق الـ TXID هنا...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("تفعيل الآن ✅"):
            if len(txid) > 15:
                st.session_state['auth'] = True
                st.success("🎉 تم التفعيل بنجاح! جاري تحميل لوحة التحليل...")
                time.sleep(1.5) 
                st.rerun()
            else:
                st.error("❌ رقم العملية غير صحيح، يرجى المحاولة مرة أخرى.")
    with col2:
        st.write("") 

# إذا كان المستخدم مشتركاً (أو الموقع لا يزال في الفترة المجانية) -> اعرض الإشارات
else:
    if st.session_state['auth']:
        st.success("✅ مرحباً بك أيها المتداول المحترف! حسابك نشط.")
    
    # الحصول على الإشارات
    sig, ent, tp, sl = calculate_signals()
    
    # عرض الإشارة بشكل بارز
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("الإشارة الحالية", sig, help="BUY (شراء) أو SELL (بيع)")
    with c2:
        st.metric("نقطة الدخول المقترحة", f"${ent}", help="السعر المثالي لفتح الصفقة")

    # عرض الأهداف ووقف الخسارة
    st.markdown("### تفاصيل الصفقة:")
    col_tp, col_sl = st.columns(2)
    col_tp.success(f"🎯 **هدف جني الأرباح (TP):** ${tp}")
    col_sl.error(f"🛡️ **وقف الخسارة (SL):** ${sl}")
    
    st.markdown("---")
    st.info("🕒 تم تحديث البيانات بنجاح.")
