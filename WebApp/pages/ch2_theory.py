import streamlit as st

st.set_page_config(page_title="Ch2: Ideas & Formulas", layout="wide")

st.title("Chapter 2: Time Value of Money")

st.header("💡 Main Covered Ideas")
st.markdown("""
The core concept of Engineering Economy is that **money has a time value**. A dollar today is worth more than a dollar tomorrow because of its potential earning capacity. 

This chapter introduces the foundational equivalence **factors** used to translate cash flows across time:
*   **Equivalence:** Determining when different sums of money at different times are equal in economic value.
*   **Simple vs. Compound Interest:** Simple interest is calculated only on the principal amount, whereas compound interest is calculated on the principal *and* accumulated interest.
*   **Cash Flow Diagrams:** Visual representations of costs (downward arrows) and revenues (upward arrows) over a timeline.
""")

st.markdown("---")
st.header("📚 Formula Sheet")
st.markdown("A quick reference guide for standard engineering economy factors and their corresponding Microsoft Excel functions.")

st.markdown("""
| Name | Notation | Equation | Excel Function |
| :--- | :---: | :---: | :--- |
| Compound Amount | $(F/P,i,n)$ | $F = P(1+i)^n$ | `=FV(i%, n, , -P)` |
| Present Worth | $(P/F,i,n)$ | $P = F(1+i)^{-n}$ | `=PV(i%, n, , -F)` |
| Uniform Series Present Worth | $(P/A,i,n)$ | $P = A [ \\frac{(1+i)^n - 1}{i(1+i)^n} ]$ | `=PV(i%, n, -A)` |
| Uniform Series Compound Amount | $(F/A,i,n)$ | $F = A [ \\frac{(1+i)^n - 1}{i} ]$ | `=FV(i%, n, -A)` |
| Capital Recovery | $(A/P,i,n)$ | $A = P [ \\frac{i(1+i)^n}{(1+i)^n - 1} ]$ | `=PMT(i%, n, -P)` |
| Sinking Fund | $(A/F,i,n)$ | $A = F [ \\frac{i}{(1+i)^n - 1} ]$ | `=PMT(i%, n, , -F)` |
| Arithmetic Gradient Present Worth | $(P/G,i,n)$ | $P_G = G [ \\frac{(1+i)^n - in - 1}{i^2(1+i)^n} ]$ | *N/A* |
| Arithmetic Gradient Uniform Series | $(A/G,i,n)$ | $A_G = G [ \\frac{1}{i} - \\frac{n}{(1+i)^n - 1} ]$ | *N/A* |
| Geometric Gradient Present Worth ($i \\neq g$) | $(P_g, A_1, g, i, n)$ | $P_g = A_1 \\left[ \\frac{\\left(\\frac{1+g}{1+i}\\right)^n - 1}{g-i} \\right]$ | *N/A* |
| Geometric Gradient Present Worth ($i = g$) | $(P_g, A_1, g, i, n)$ | $P_g = \\frac{n A_1}{1+i}$ | *N/A* |
""")

st.info("Note: In Excel functions, present values (P), future values (F), and payments (A) must follow standard cash flow conventions. An investment is entered as a negative number (e.g., `-P`) to yield a positive return.")
