import streamlit as st
import json
import os
from datetime import date

FILE = "expenses.json"

def load_expenses():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="مصاريفي", page_icon="💰")
st.title("💰 برنامج حساب المصاريف")

expenses = load_expenses()

# --- إضافة مصروف ---
st.header("إضافة مصروف")

with st.form("add_form"):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("المبلغ", min_value=0.0, step=0.5)
        category = st.selectbox(
            "التصنيف",
            ["طعام", "مواصلات", "فواتير", "تسوق", "صحة", "أخرى"]
        )
    with col2:
        note = st.text_input("ملاحظة (اختياري)")
        d = st.date_input("التاريخ", value=date.today())

    submitted = st.form_submit_button("إضافة")

    if submitted:
        if amount <= 0:
            st.error("اكتب مبلغ صحيح")
        else:
            expenses.append({
                "amount": amount,
                "category": category,
                "note": note,
                "date": str(d)
            })
            save_expenses(expenses)
            st.success("تمت الإضافة ✅")
            st.rerun()

# --- عرض المصاريف ---
st.header("المصاريف")

if expenses:
    total = sum(e["amount"] for e in expenses)
    st.metric("الإجمالي", f"{total:.2f}")

    # الإجمالي حسب التصنيف
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    st.bar_chart(totals)

    st.dataframe(expenses, use_container_width=True)

    # حذف
    st.subheader("حذف مصروف")
    idx = st.number_input(
        "رقم المصروف",
        min_value=1,
        max_value=len(expenses),
        step=1
    )
    if st.button("حذف"):
        expenses.pop(idx - 1)
        save_expenses(expenses)
        st.success("تم الحذف")
        st.rerun()
else:
    st.info("لا توجد مصاريف بعد.")
