import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# تعريف الدوال الرياضية والمشتقات
def func(x):
    return x**3 - 6*x**2 + 9*x + 1  # مثال لدالة رياضية

def first_derivative(x):
    return 3*x**2 - 12*x + 9  # المشتقة الأولى للدالة

def second_derivative(x):
    return 6*x - 12  # المشتقة الثانية للدالة

# إعداد الواجهة
def plot_graph():
    x = np.linspace(-2, 6, 400)
    y = func(x)
    y_prime = first_derivative(x)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, label=r'$\mathbf{f(x) = x^3 - 6x^2 + 9x + 1}$', color='blue')
    ax.plot(x, y_prime, label=r'$\mathbf{f\'(x) = 3x^2 - 12x + 9}$', color='red')

    # تخصيص الرسم
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    
    st.pyplot(fig)

# عرض السؤال والأسئلة الاختيارية
def create_question():
    st.title("اختبار قراءة التمثيل البياني للمشتقات")

    # عرض السؤال بالعربية والإنجليزية
    st.subheader("السؤال بالعربية:")
    st.write("ما هي النقاط الحرجة لهذه الدالة؟")
    
    st.subheader("Question in English:")
    st.write("What are the critical points for this function?")
    
    # رسم المشتقة
    plot_graph()
    
    # المعادلة الرياضية بصيغة MathJax:
    st.latex(r"""
    f(x) = x^3 - 6x^2 + 9x + 1
    """)
    st.latex(r"""
    f'(x) = 3x^2 - 12x + 9
    """)

    # الخيارات المتعددة
    options = ["x = 1", "x = 2", "x = 3", "x = 4"]
    answer = st.radio("اختر إجابتك", options, index=1)  # الافتراضي هو الخيار الثاني (x = 2)
    
    # زر التحقق
    if st.button("تحقق"):
        correct_answer = "x = 2"
        if answer == correct_answer:
            st.success("إجابة صحيحة!")
        else:
            st.error("الإجابة غير صحيحة. حاول مرة أخرى.")

# تنفيذ التطبيق
if __name__ == "__main__":
    create_question()
