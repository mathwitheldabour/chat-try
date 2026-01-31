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

# إعداد الرسومات
def plot_derivative(derivative_func):
    x = np.linspace(-2, 6, 400)
    y = derivative_func(x)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, label=r"$f'(x)$", color='red')

    # تحديد مقياس الرسم ليكون على المحاور
    ax.set_xlim([-2, 6])
    ax.set_ylim([-10, 10])
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("f'(x)")
    ax.legend()
    
    st.pyplot(fig)

# عرض رأس السؤال بشكل جدول (العربي والإنجليزي معًا)
def display_question(question_arabic, question_english):
    st.markdown(f"""
    <table style="width:100%">
      <tr>
        <td style="text-align: right; width: 50%;">{question_arabic}</td>
        <td style="text-align: left; width: 50%;">{question_english}</td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

# الأسئلة المختلفة
def create_question_1():
    question_arabic = "ما هي النقاط الحرجة لهذه الدالة؟"
    question_english = "What are the critical points for this function?"

    display_question(question_arabic, question_english)
    
    plot_derivative(first_derivative)  # رسم المشتقة الأولى فقط
    
    options = ["x = 1", "x = 2", "x = 3", "x = 4"]
    answer = st.radio("اختر إجابتك", options, index=1)
    
    if st.button("تحقق"):
        correct_answer = "x = 2"
        if answer == correct_answer:
            st.success("إجابة صحيحة!")
        else:
            st.error("الإجابة غير صحيحة. حاول مرة أخرى.")

def create_question_2():
    question_arabic = "هل هذه المشتقة تمثل زيادة أم نقصان؟"
    question_english = "Does this derivative represent increase or decrease?"

    display_question(question_arabic, question_english)
    
    plot_derivative(first_derivative)  # رسم المشتقة الأولى فقط
    
    options = ["زيادة", "نقصان"]
    answer = st.radio("اختر إجابتك", options, index=0)
    
    if st.button("تحقق"):
        correct_answer = "زيادة"
        if answer == correct_answer:
            st.success("إجابة صحيحة!")
        else:
            st.error("الإجابة غير صحيحة. حاول مرة أخرى.")

def create_question_3():
    question_arabic = "ما هي المشتقة الثانية لهذه الدالة؟"
    question_english = "What is the second derivative for this function?"

    display_question(question_arabic, question_english)
    
    plot_derivative(second_derivative)  # رسم المشتقة الثانية فقط
    
    options = ["f''(x) = 6x - 12", "f''(x) = 6x^2 - 12", "f''(x) = 6x^2 + 12", "f''(x) = 12x - 12"]
    answer = st.radio("اختر إجابتك", options, index=0)
    
    if st.button("تحقق"):
        correct_answer = "f''(x) = 6x - 12"
        if answer == correct_answer:
            st.success("إجابة صحيحة!")
        else:
            st.error("الإجابة غير صحيحة. حاول مرة أخرى.")

# التنقل بين الأسئلة
def main():
    questions = {
        "سؤال 1": create_question_1,
        "سؤال 2": create_question_2,
        "سؤال 3": create_question_3
    }

    question = st.selectbox("اختر السؤال", list(questions.keys()))
    questions[question]()

if __name__ == "__main__":
    main()
