import streamlit as st

st.set_page_config(page_title="Ch1: Ideas & Formulas", layout="wide")

st.title("Chapter 1: Foundation of Engineering Economy")

st.header("💡 Main Covered Ideas")
st.markdown("""
The foundation of engineering economy is about **deciding** where and how to invest **capital funds** to **add value** in the future. Tackling a capital investment requires a structured approach.

### 1. The Engineering Economy Workflow
Real-world problems require a 9-step structured approach, typically grouped into three phases:
*   **Phase 1: The Foundation:** Identify the problem, gather relevant data, and creatively develop alternatives (including the "Do Nothing" alternative).
*   **Phase 2: Mathematical Modelling & Evaluation:** Translate alternatives into cash flows and apply economic criteria to evaluate them objectively.
*   **Phase 3: Action & Accountability:** Implement the best solution, monitor its real-world results, and refine it over time.

### 2. Cash Flows
Cash flows are the amounts of money estimated for future projects or observed for past events.
*   **Cash Inflows (+):** Receipts, revenues, incomes, and savings. (Upward arrows on a cash flow diagram).
*   **Cash Outflows (-):** Costs, disbursements, expenses, and taxes. (Downward arrows on a cash flow diagram).

### 3. Minimum Attractive Rate of Return (MARR)
For any investment to be profitable, it must return a **fair** rate.
*   The **MARR** is a reasonable rate of return established for the evaluation of alternatives.
*   A project is economically viable **if and only if** its Rate of Return $\\geq$ MARR.
*   MARR is influenced by the **Cost of Capital** (the blended cost of equity and debt financing), project risk, and opportunity costs.

### 4. Simple vs. Compound Interest
*   **Simple Interest:** Calculated using the principal only.
*   **Compound Interest:** Calculated on the principal *plus* the accumulated interest of previous periods ("interest on interest").

### 5. The Rule of 72
*   A mathematical approximation used to estimate how long it will take for an investment (or debt) to exactly **double** in value.
*   Calculated by simply dividing 72 by the annual compound interest rate (expressed as a whole number).
""")

st.markdown("---")
st.header("📚 Formula Sheet")

st.markdown("""
| Name | Equation | Description |
| :--- | :--- | :--- |
| **Interest Rate (%)** | $\\frac{\\text{final} - \\text{principal}}{\\text{principal}} \\times 100\\%$ | For borrowing money |
| **Rate of Return (%)** | $\\frac{\\text{total investment value} - \\text{principal}}{\\text{principal}} \\times 100\\%$ | For investing/saving money |
| **Simple Interest** | $F = P(1+ni)$ | $P$ = Principal, $n$ = periods, $i$ = interest rate |
| **Compound Interest** | $F = P(1+i)^n$ | Used in almost all standard engineering economy problems |
| **Rule of 72** | $n \\approx \\frac{72}{i\\%}$ | Mental math shortcut: Years to double an investment |
""")

st.info("Note: When using the Rule of 72, the interest rate $i$ should be entered as a whole number (e.g., $9$ for 9%), not a decimal ($0.09$).")
