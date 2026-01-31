import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import time
from fpdf import FPDF
import random

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="Math Master: Critical Points", layout="wide", page_icon="📈")

if 'language' not in st.session_state:
    st.session_state.language = 'Arabic'
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# Translation Dictionary
TRANS = {
    'Arabic': {
        'title': 'التفاضل: النقاط الحرجة وفترات التزايد',
        'teacher': 'إعداد: أ. إبراهيم',
        'nav_home': 'شرح المفهوم',
        'nav_train': 'تدريب (10 أسئلة)',
        'nav_test': 'الاختبار النهائي (20 دقيقة)',
        'start_test': 'ابدأ الاختبار',
        'submit': 'إرسال الإجابة',
        'next': 'السؤال التالي',
        'explain': 'الشرح:',
        'correct': '✅ إجابة صحيحة!',
        'wrong': '❌ إجابة خاطئة.',
        'gen_pdf': 'طباعة ورقة عمل (PDF)',
        'contact': 'تواصل عبر واتساب',
        'graph_orig': 'الدالة الأصلية',
        'graph_deriv': 'رسم المشتقة',
        'find_crit': 'أوجد النقاط الحرجة للدالة:',
        'find_inc': 'أوجد فترات التزايد للدالة:',
        'find_k': 'إذا كانت x=2 نقطة حرجة للدالة أدناه، أوجد قيمة k:',
    },
    'English': {
        'title': 'Calculus: Critical Points & Intervals',
        'teacher': 'By: Mr. Ibrahim',
        'nav_home': 'Concept Guide',
        'nav_train': 'Training (10 Qs)',
        'nav_test': 'Final Exam (20 mins)',
        'start_test': 'Start Test',
        'submit': 'Submit Answer',
        'next': 'Next Question',
        'explain': 'Explanation:',
        'correct': '✅ Correct!',
        'wrong': '❌ Wrong.',
        'gen_pdf': 'Generate Worksheet (PDF)',
        'contact': 'Contact via WhatsApp',
        'graph_orig': 'Original Function',
        'graph_deriv': 'Derivative Graph',
        'find_crit': 'Find critical points for:',
        'find_inc': 'Find increasing intervals for:',
        'find_k': 'If x=2 is a critical point for the function below, find k:',
    }
}

def t(key):
    return TRANS[st.session_state.language][key]

# --- 2. MATH ENGINE (SYMPY) ---
def generate_problem(q_type):
    x, k = sp.symbols('x k')
    
    # Type 1: Simple Polynomial Critical Points
    if q_type == 'poly_crit':
        a = random.randint(1, 3)
        b = random.randint(-6, 6)
        c = random.randint(-10, 10)
        func = a*(x**3)/3 + b*(x**2)/2 + c*x 
        deriv = sp.diff(func, x)
        crit_points = sp.solve(deriv, x)
        
        question_text = f"{t('find_crit')} $$f(x) = {sp.latex(func)}$$"
        correct = [float(p.evalf()) for p in crit_points]
        correct = [round(v, 2) for v in correct]
        correct.sort()
        
        # Distractors
        options = [
            f"{correct}",
            f"{[round(v + 1, 2) for v in correct]}",
            f"{[round(v * -1, 2) for v in correct]}",
            f"{[round(v/2, 2) for v in correct]}"
        ]
        random.shuffle(options)
        return {"q": question_text, "func": func, "correct": str(correct), "options": options, "type": "poly"}

    # Type 2: Find Constant k
    elif q_type == 'find_k':
        target_crit = random.randint(1, 5)
        # f(x) = x^2 + kx
        func_k = x**2 + k*x
        deriv_k = sp.diff(func_k, x) # 2x + k
        # at x = target, 2(target) + k = 0 -> k = -2*target
        ans_k = -2 * target_crit
        
        func_display = func_k.subs(k, sp.Symbol('k'))
        question_text = f"{t('find_k')} $$f(x) = {sp.latex(func_display)}$$"
        
        options = [str(ans_k), str(ans_k * -1), str(ans_k + 2), str(0)]
        random.shuffle(options)
        return {"q": question_text, "func": func_display, "correct": str(ans_k), "options": options, "type": "constant"}
    
    return None

# --- 3. GRAPHING UTILS ---
def plot_func(expr, title):
    x_vals = np.linspace(-5, 5, 400)
    f = sp.lambdify(sp.Symbol('x'), expr, 'numpy')
    y_vals = f(x_vals)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x_vals, y_vals, color='#4CAF50', linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(title)
    return fig

# --- 4. PDF GENERATOR ---
def create_worksheet():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Calculus Worksheet - Mr. Ibrahim", ln=1, align='C')
    pdf.ln(10)
    
    for i in range(1, 6):
        prob = generate_problem('poly_crit')
        # Note: FPDF doesn't render LaTeX, needs basic text
        pdf.cell(200, 10, txt=f"Q{i}: Find critical points for the function.", ln=1)
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 5. UI COMPONENTS ---

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3771/3771278.png", width=100)
    st.title(t('teacher'))
    
    # Language Toggle
    lang = st.radio("Language / اللغة", ['Arabic', 'English'])
    st.session_state.language = lang
    st.write("---")
    
    nav = st.radio("القائمة / Menu", ['Home', 'Practice', 'Test'])
    st.session_state.page = nav
    
    st.write("---")
    st.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/123456789)")

# PAGE: HOME (Explanation)
if st.session_state.page == 'Home':
    st.header(t('title'))
    st.markdown("""
    ### 📘 Concept Guide / شرح المفهوم
    
    **1. Critical Points / النقاط الحرجة:**
    Values of $x$ in the domain of $f$ where $f'(x) = 0$ or $f'(x)$ is undefined.
    
    **2. Steps to Solve / خطوات الحل:**
    1. Find the derivative $f'(x)$.
    2. Set $f'(x) = 0$ and solve for $x$.
    3. Check where $f'(x)$ does not exist.
    """)
    
    # Interactive Example
    st.subheader("🧪 Interactive Lab")
    expr_input = st.text_input("Enter a function (e.g., x**3 - 3*x):", "x**3 - 3*x")
    if expr_input:
        try:
            x = sp.Symbol('x')
            user_expr = sp.sympify(expr_input)
            user_deriv = sp.diff(user_expr, x)
            
            col1, col2 = st.columns(2)
            with col1:
                st.latex(f"f(x) = {sp.latex(user_expr)}")
                st.latex(f"f'(x) = {sp.latex(user_deriv)}")
                
                # Solve
                crits = sp.solve(user_deriv, x)
                st.info(f"Critical Points at x = {crits}")
                
            with col2:
                st.pyplot(plot_func(user_expr, t('graph_orig')))
                
        except:
            st.error("Invalid equation format.")

# PAGE: PRACTICE (Training)
elif st.session_state.page == 'Practice':
    st.header(t('nav_train'))
    
    if 'current_q' not in st.session_state:
        st.session_state.current_q = generate_problem(random.choice(['poly_crit', 'find_k']))
        
    q = st.session_state.current_q
    
    st.markdown(f"### {q['q']}")
    
    user_ans = st.radio("Choose:", q['options'])
    
    if st.button(t('submit')):
        if user_ans == q['correct']:
            st.success(t('correct'))
            st.balloons()
        else:
            st.error(t('wrong'))
            st.warning(f"{t('explain')} \n Correct answer is {q['correct']}")
            # Here we could show steps using SymPy logic
            
    if st.button(t('next')):
        st.session_state.current_q = generate_problem(random.choice(['poly_crit', 'find_k']))
        st.rerun()

# PAGE: TEST (Timed)
elif st.session_state.page == 'Test':
    st.header(t('nav_test'))
    
    # Timer Logic (Simplified for demo)
    if 'start_time' not in st.session_state:
        st.button(t('start_test'), on_click=lambda: st.session_state.update({'start_time': time.time(), 'test_qs': [generate_problem('poly_crit') for _ in range(5)]}))
    else:
        elapsed = time.time() - st.session_state.start_time
        remaining = 1200 - elapsed # 20 mins
        
        if remaining <= 0:
            st.error("Time is up!")
        else:
            st.progress(int((remaining/1200)*100))
            st.caption(f"Time Left: {int(remaining//60)} min {int(remaining%60)} sec")
            
            # Display Questions Loop (Simplified)
            answers = {}
            for i, q in enumerate(st.session_state.test_qs):
                st.markdown(f"**Q{i+1}:** {q['q']}")
                answers[i] = st.radio(f"Select for Q{i+1}", q['options'], key=f"test_{i}")
                st.write("---")
            
            if st.button("Finish Exam"):
                score = 0
                report = []
                for i, q in enumerate(st.session_state.test_qs):
                    if answers[i] == q['correct']:
                        score += 1
                    else:
                        report.append(f"Q{i+1}: Failed (Topic: {q['type']})")
                
                st.success(f"Score: {score}/5")
                if report:
                    st.warning("Weak Areas:\n" + "\n".join(report))
                    
                # Download PDF Button
                pdf_bytes = create_worksheet()
                st.download_button(label=t('gen_pdf'), data=pdf_bytes, file_name="worksheet.pdf", mime='application/pdf')