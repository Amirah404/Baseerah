# إعداد: أميره شايم الرشيدي - مشروع بَصِيرَة
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
import os # تم إضافة هذه المكتبة لضمان أمان المسارات

st.set_page_config(page_title="بَصِيرَة | نظام الإنذار المبكر", page_icon="🔮", layout="wide")

# تصميم CSS ذكي: يصلح النصوص العربية ويبقي القائمة يساراً بدون تخريب
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, div, label, p { 
        font-family: 'Tajawal', sans-serif !important;
    }
    
    /* توجيه النصوص فقط لليمين لضبط علامات الترقيم */
    .stMarkdown, label, .stMetric, .stAlert {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* ضبط القوائم المنسدلة ومدخلات الأرقام */
    div[data-baseweb="select"] > div, input {
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* زر التوليد */
    .stButton>button {
        background-color: #0F172A; color: white; border-radius: 8px;
        padding: 10px 24px; font-weight: bold; border: 1px solid #38BDF8; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #38BDF8; color: #0F172A; transform: scale(1.02); }
    
    /* الروابط */
    .contact-links a {
        color: #0284C7; text-decoration: none; font-weight: bold; margin-left: 15px; font-size: 16px;
    }
    .contact-links a:hover { color: #0369A1; text-decoration: underline; }
    </style>
""", unsafe_allow_html=True)

def safe_int(val):
    if pd.isna(val) or np.isnan(val):
        return 0
    return int(val)

@st.cache_data
def load_data():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../data/Kafaat_Cleaned.csv')
    
    if not os.path.exists(file_path):
        file_path = 'data/Kafaat_Cleaned.csv'
        
    try:
        data = pd.read_csv(file_path)
        data['Program Type'] = data['Program Type'].astype(str).str.strip()
        data['Program Name'] = data['Program Name'].astype(str).str.strip()
        
        # --- تعديل المستشارة 1: توحيد مسمى 'عن بعد' لحل مشكلة التصفية ---
        data['Program Type'] = data['Program Type'].str.replace('عن بُعد', 'عن بعد').str.replace('عن  بعد', 'عن بعد')
        
        return data
    except Exception as e:
        st.error(f"حدث خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

df = load_data()
if not df.empty:
    program_names = df['Program Name'].unique().tolist()
else:
    program_names = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3208/3208405.png", width=100)
st.sidebar.title("☰ القائمة الرئيسية")
page = st.sidebar.radio("اختر صفحة النظام:\u200F", 
                        ["🔮 أداة التنبؤ الذكية", 
                         "📊 لوحة البيانات التفاعلية", 
                         "🤖 المستشار الذكي (Beta)",
                         "❓ الأسئلة الشائعة"])

# ================= الصفحة الأولى: أداة التنبؤ =================
if page == "🔮 أداة التنبؤ الذكية":
    st.title("🔮 أداة الإنذار المبكر (محاكي القرارات)")
    st.markdown("<p>اختبر برامج الجمعية قبل إطلاقها لتوقع نسبة الالتزام ومنع الهدر المالي.</p>", unsafe_allow_html=True)
    
    # --- تعديل المستشارة 2: توضيح شفافية أداة المحاكاة للجنة التحكيم ---
    st.info("💡 ملاحظة: الأرقام الناتجة عن أداة التنبؤ أدناه هي أرقام (تجريبية/محاكاة) لاختبار كفاءة الخوارزمية. عند ربط النظام ببيانات 'الحضور الفعلي' للجمعية، سيقوم بحساب النسب الحقيقية وتقديم التوصيات بدقة.")

    col1, col2, col3 = st.columns(3)
    prog_name = col1.selectbox("اختر البرنامج:\u200F", program_names)
    prog_type = col2.selectbox("بيئة التنفيذ:\u200F", ["حضوري", "عن بعد"])
    target_ben = col3.number_input("العدد المستهدف:\u200F", min_value=10, max_value=5000, value=150)
    
    if st.button("توليد التنبؤ الذكي ⚙️", use_container_width=True):
        with st.spinner('بَصِيرَة تحلل البيانات... 👁️'):
            time.sleep(1)
            
        base_commitment = np.random.randint(75, 95) if prog_type == "حضوري" else np.random.randint(55, 80)
        expected_dropouts = int(target_ben * ((100 - base_commitment) / 100))
        
        st.divider()
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = base_commitment,
            # --- تعديل المستشارة 3: تغيير المسميات لتصبح واضحة أنها محاكاة ---
            title = {'text': "نسبة الالتزام (محاكاة/تجريبية) %", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0F172A"},
                'steps': [
                    {'range': [0, 60], 'color': "#EF4444"},
                    {'range': [60, 80], 'color': "#F59E0B"},
                    {'range': [80, 100], 'color': "#10B981"}
                ]}
        ))
        
        left_col, right_col = st.columns([1, 1])
        with left_col:
            st.plotly_chart(fig_gauge, use_container_width=True)
        with right_col:
            st.markdown(f"<h3>🎯 تحليل برنامج: {prog_name}</h3>", unsafe_allow_html=True)
            st.metric("المستفيدين الملتزمين", f"{target_ben - expected_dropouts}")
            # --- تعديل المستشارة 3: تغيير المسميات ---
            st.metric("التسرب المتوقع (بالمحاكاة)", f"{expected_dropouts} مستفيد")
            
            if base_commitment >= 80:
                st.success("✅ **توصية:** يعتمد البرنامج. مخاطر الهدر منخفضة.\u200F")
            elif base_commitment >= 65:
                st.warning("⚠️ **توصية:** يمكن اعتماده مع خطة لتحفيز الحضور.\u200F")
            else:
                st.error("❌ **توصية:** خطر هدر مالي! يرجى تحويله لحضوري.\u200F")

# ================= الصفحة الثانية: الداشبورد المطوّر =================
elif page == "📊 لوحة البيانات التفاعلية":
    st.title("📊 لوحة الأداء التاريخي")
    st.markdown("<p>استخدم الفلاتر أدناه لتخصيص عرض البيانات الفعلية للجمعية.</p>", unsafe_allow_html=True)
    
    f_col1, f_col2 = st.columns(2)
    filter_type = f_col1.radio("تصفية حسب بيئة البرنامج:\u200F", ["الكل", "حضوري", "عن بعد"], horizontal=True)
    filter_prog = f_col2.selectbox("تصفية حسب اسم البرنامج:\u200F", ["الكل"] + program_names)
    
    if not df.empty:
        filtered_df = df.copy()
        if filter_type != "الكل":
            filtered_df = filtered_df[filtered_df['Program Type'] == filter_type]
        if filter_prog != "الكل":
            filtered_df = filtered_df[filtered_df['Program Name'] == filter_prog]
        
        if filtered_df.empty:
            st.warning("لا توجد بيانات مطابقة لهذه الفلاتر.\u200F")
        else:
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("إجمالي المستفيدين", f"{filtered_df['Number of Beneficiaries'].sum():,}")
            
            # حماية الكود من الخطأ إذا لم يكن عمود Commitment_Index موجوداً
            if 'Commitment_Index' in filtered_df.columns:
                avg_commitment = safe_int(filtered_df['Commitment_Index'].mean())
                kpi2.metric("متوسط الالتزام (محاكاة)", f"{avg_commitment}%")
            else:
                kpi2.metric("متوسط الالتزام", "غير متوفر")
                
            if 'Expected_Dropouts' in filtered_df.columns:
                kpi3.metric("إجمالي التسرب (محاكاة)", f"{filtered_df['Expected_Dropouts'].sum():,}")
            else:
                kpi3.metric("إجمالي التسرب", "غير متوفر")
            
            st.divider()
            
            # المنطق للاستنتاجات الذكية (محمية في حال عدم وجود الأعمدة)
            if 'Commitment_Index' in df.columns:
                if filter_prog != "الكل":
                    prog_df = df[df['Program Name'] == filter_prog]
                    onsite_val = safe_int(prog_df[prog_df['Program Type'] == 'حضوري']['Commitment_Index'].mean())
                    online_val = safe_int(prog_df[prog_df['Program Type'] == 'عن بعد']['Commitment_Index'].mean())
                    
                    if onsite_val > online_val and online_val > 0:
                        st.success(f"💡 **استنتاج ذكي:** برنامج '{filter_prog}' يحقق نتائج أفضل بكثير عند تنفيذه (حضورياً) بنسبة التزام {onsite_val}% مقارنة بـ {online_val}% (عن بعد).\u200F")
                    elif online_val > onsite_val and onsite_val > 0:
                        st.success(f"💡 **استنتاج ذكي:** برنامج '{filter_prog}' يحقق نتائج أفضل عند تنفيذه (عن بعد) بنسبة التزام {online_val}% مقارنة بـ {onsite_val}% (حضورياً).\u200F")
                    elif onsite_val > 0 and online_val == 0:
                        st.info(f"💡 **استنتاج ذكي:** برنامج '{filter_prog}' نُفذ (حضورياً) فقط بنسبة التزام {onsite_val}%. ينصح بالاستمرار على هذه البيئة.\u200F")
                    elif online_val > 0 and onsite_val == 0:
                        st.info(f"💡 **استنتاج ذكي:** برنامج '{filter_prog}' نُفذ (عن بعد) فقط بنسبة التزام {online_val}%.\u200F")
                else:
                    onsite_all = safe_int(df[df['Program Type'] == 'حضوري']['Commitment_Index'].mean())
                    online_all = safe_int(df[df['Program Type'] == 'عن بعد']['Commitment_Index'].mean())
                    st.info(f"💡 **استنتاج عام:** تاريخياً، البرامج الحضورية تتفوق بنسبة التزام ({onsite_all}%) مقارنة بالبرامج عن بعد ({online_all}%).\u200F")
            
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                if 'Expected_Dropouts' in filtered_df.columns:
                    fig_bar = px.bar(filtered_df.sort_values('Expected_Dropouts', ascending=False).head(5), 
                                     x='Program Name', y='Expected_Dropouts', title="أعلى البرامج في التسرب المتوقع")
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.write("بيانات التسرب غير متوفرة للرسم.")
                    
            with col_chart2:
                fig_pie = px.pie(filtered_df, names='Program Type', values='Number of Beneficiaries', title="توزيع المستفيدين")
                st.plotly_chart(fig_pie, use_container_width=True)
                
            csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل هذا التقرير (CSV)\u200F", data=csv, file_name='Filtered_Report.csv', mime='text/csv')
    else:
        st.error("تعذر تحميل البيانات لعرض اللوحة.")

# ================= الصفحة الثالثة: المستشار الذكي المتطور =================
elif page == "🤖 المستشار الذكي (Beta)":
    st.title("🤖 مساعد بَصِيرَة الآلي")
    st.markdown("<p>تحدث مع النظام مباشرة للحصول على تحليلات فورية من بيانات الجمعية.</p>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "مرحباً بك! أنا مساعد بصيرة. يمكنك سؤالي عن: أسوأ برنامج، ملخص البرامج الحضورية، أو إجمالي المستفيدين.\u200F"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"<p>{message['content']}</p>", unsafe_allow_html=True)

    prompt = st.chat_input("اكتب سؤالك هنا...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<p>{prompt}</p>", unsafe_allow_html=True)
            
        response = ""
        if not df.empty:
            if "سلام" in prompt or "مرحبا" in prompt or "هلا" in prompt:
                response = "وعليكم السلام! أهلاً بك في نظام بصيرة. تفضل، كيف يمكنني مساعدة متخذ القرار اليوم؟\u200F"
            elif "عاجل" in prompt or "أسوأ" in prompt or "تسرب" in prompt or "خطر" in prompt:
                if 'Commitment_Index' in df.columns:
                    worst_prog = df.sort_values('Commitment_Index').iloc[0]
                    response = f"أكثر برنامج يحتاج تدخل هو **{worst_prog['Program Name']}** حيث أن مؤشر التزامه (بالمحاكاة) هو {worst_prog['Commitment_Index']}% فقط.\u200F"
                else:
                    response = "بيانات مؤشر الالتزام غير متوفرة للإجابة على هذا السؤال."
            elif "حضوري" in prompt:
                onsite_df = df[df['Program Type'] == 'حضوري']
                if 'Commitment_Index' in onsite_df.columns:
                    avg_onsite = safe_int(onsite_df['Commitment_Index'].mean())
                    response = f"البرامج الحضورية يبلغ متوسط التزامها {avg_onsite}%، بإجمالي {onsite_df['Number of Beneficiaries'].sum():,} مستفيد.\u200F"
                else:
                    response = f"يوجد إجمالي {onsite_df['Number of Beneficiaries'].sum():,} مستفيد في البرامج الحضورية.\u200F"
            elif "عن بعد" in prompt or "عن بُعد" in prompt:
                online_df = df[df['Program Type'] == 'عن بعد']
                if 'Commitment_Index' in online_df.columns:
                    avg_online = safe_int(online_df['Commitment_Index'].mean())
                    response = f"البرامج عن بعد يبلغ متوسط التزامها {avg_online}%، بإجمالي {online_df['Number of Beneficiaries'].sum():,} مستفيد.\u200F"
                else:
                    response = f"يوجد إجمالي {online_df['Number of Beneficiaries'].sum():,} مستفيد في البرامج عن بعد.\u200F"
            elif "إجمالي" in prompt or "مستفيد" in prompt or "عدد" in prompt:
                total_ben = df['Number of Beneficiaries'].sum()
                response = f"إجمالي عدد المستفيدين في جميع برامج الجمعية هو {total_ben:,} مستفيد.\u200F"
            elif "برامج" in prompt or "برنامج" in prompt:
                response = "لدينا نوعان من البرامج. هل تبحث عن تفاصيل 'البرامج الحضورية' أم 'البرامج عن بُعد'؟ أو هل تريد معرفة 'أسوأ برنامج'؟\u200F"
            elif "كفاءات" in prompt or "جمعية" in prompt:
                response = "جمعية كفاءات تسعى لتقليل الهدر المالي. يمكنك سؤالي عن إجمالي المستفيدين أو تحليل برامجها.\u200F"
            else:
                response = "عذراً، لم أتعرف على هذا الطلب بدقة. جرب سؤالي بكلمات مثل: 'أسوأ برنامج'، 'البرامج الحضورية'، أو 'إجمالي المستفيدين'.\u200F"
        else:
            response = "عذراً، لا توجد بيانات متاحة حالياً لتحليلها."
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(f"<p>{response}</p>", unsafe_allow_html=True)

# ================= الصفحة الرابعة: الأسئلة الشائعة =================
elif page == "❓ الأسئلة الشائعة":
    st.title("❓ الأسئلة الشائعة")
    st.markdown("<p>تم تطوير هذا النظام كحل ابتكاري استجابةً لتحدي تحليل البيانات في القطاع غير الربحي.</p>", unsafe_allow_html=True)
    
    with st.expander("📌 ما هو الهدف من مشروع بَصِيرَة؟", expanded=True):
        st.markdown("<p>يهدف المشروع إلى توفير نظام إنذار مبكر للجمعيات الأهلية (مثل جمعية كفاءات)، حيث يحلل البيانات التاريخية للمستفيدين لبناء مؤشر يسمى 'مؤشر الالتزام'. يساعد هذا المؤشر متخذي القرار في التنبؤ بنسب التسرب وتقليل الهدر المالي قبل اعتماد ميزانيات البرامج الجديدة.</p>", unsafe_allow_html=True)
        
    with st.expander("💡 كيف تعمل أداة التنبؤ الذكية؟"):
        st.markdown("<p>تعتمد الأداة حالياً على محاكاة تجريبية بُنيت بلغة البرمجة (بايثون)، حيث تقارن نوع البرنامج (حضوري أو عن بعد) والعدد المستهدف، لتقديم توصية فورية. وعند ربطها ببيانات الحضور الفعلي للجمعية، ستقدم تنبؤات حقيقية دقيقة.</p>", unsafe_allow_html=True)
        
    with st.expander("👩‍💻 من هي مطورة النظام؟"):
        st.markdown("<p>تم هندسة البيانات، وتطوير خوارزميات التنبؤ، وبناء هذه الواجهة التفاعلية بواسطة <b>أميره شايم الرشيدي</b>، كجزء من مسابقة تحليل البيانات في القطاع غير الربحي لعام 2026.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='contact-links'>
            <p><b>للتواصل والاطلاع على الأعمال:</b></p>
           <a href="https://amirah-alreshidi.vercel.app/" target="_blank">🌐 الموقع الشخصي</a> |
           <a href="https://www.linkedin.com/in/amirah-alreshidi-ds" target="_blank">💼 لينكد إن</a> |
           <a href="https://github.com/Amirah404" target="_blank">💻 حساب GitHub</a> |
           <a href="mailto:amirah.alrshidi.ds@gmail.com" target="_blank">✉️ الإيميل</a> |
           <a href="https://wa.me/966592192622" target="_blank">📱 واتساب</a>
        </div>
        """, unsafe_allow_html=True)