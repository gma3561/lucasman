import streamlit as st
import pandas as pd

from utils.constants import PAGE_CONFIG
from utils.styles import HIDE_STREAMLIT_STYLE, MAIN_CSS
from calculators.tax import calc_tax
from calculators.deductions import calc_total_deductions

def setup_page():
    for key, value in PAGE_CONFIG.items():
        st.set_page_config(**{key: value})
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)
    st.markdown(MAIN_CSS, unsafe_allow_html=True)

def format_number(number):
    return f"{number:,.0f}원"

def main():
    setup_page()
    st.markdown('<h1 class="main-header">벤처투자 소득공제 시뮬레이터</h1>', unsafe_allow_html=True)
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    income = st.number_input("연간 총급여액", min_value=0, value=50000000, step=1000000, format="%d")
    credit_card_usage = st.number_input("신용카드 등 사용금액", min_value=0, value=20000000, step=1000000, format="%d")
    st.markdown('</div>', unsafe_allow_html=True)
    total_deductions, deduction_details = calc_total_deductions(income, credit_card_usage)
    taxable_income = max(0, income - total_deductions)
    tax = calc_tax(taxable_income)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'"""<div class="metric-card primary"><h3>총공제금액</h3><p class="amount">{format_number(total_deductions)}</p></div>"""', unsafe_allow_html=True)
    with col2:
        st.markdown(f'"""<div class="metric-card accent"><h3>산출세액</h3><p class="amount">{format_number(tax)}</p></div>"""', unsafe_allow_html=True)
    st.markdown('<div class="deduction-details">', unsafe_allow_html=True)
    st.markdown('### 공제 상세내역')
    for item, amount in deduction_details.items():
        st.markdown(f'"""<div class="detail-card"><span class="detail-label">{item}</span><span class="detail-amount">{format_number(amount)}</span></div>"""', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()