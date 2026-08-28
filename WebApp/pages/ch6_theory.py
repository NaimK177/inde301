import streamlit as st

st.set_page_config(page_title="Ch6: Main Ideas & Formulas", layout="wide")

st.title("💡 Chapter 6: Annual Worth Analysis")

st.markdown("""
Annual Worth (AW) analysis expresses all cash flows of an alternative as an **equivalent uniform annual amount** over a specified period.
It is mathematically equivalent to Present Worth (PW) and Future Worth (FW) criteria:

$$
AW = PW \\times (A/P, i, n) = FW \\times (A/F, i, n)
$$
""")

st.markdown("---")

# Section 1: Key Advantages
st.header("1. Core Advantages of Annual Worth Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Ease of Interpretation")
    st.markdown("""
    * AW is expressed in **dollars per year** ($/year).
    * Corresponds directly to corporate annual operating budgets, P&L statements, and financial reports.
    * Far easier for management and non-financial stakeholders to grasp than massive present-value lump sums.
    """)

with col2:
    st.subheader("⚡ Single Life Cycle Advantage")
    st.markdown("""
    * **No need to find the LCM:** AW must be calculated for **only one life cycle** ($n$ years) of each alternative.
    * The AW value calculated for one life cycle is **identical** to the AW value calculated over $2, 3,$ or any repeated number of cycles ($AW_{\\text{1-cycle}} = AW_{\\text{LCM}}$).
    * Eliminates the tedious multi-cycle timeline expansion required in PW analysis.
    """)

st.markdown("---")

# Section 2: Repeatability Assumptions
st.header("2. Fundamental Repeatability Assumptions")
st.markdown("""
The mathematical validity of comparing alternatives based on a single life cycle rests on three assumptions:
1. **Equal-Service Requirement:** The service provided by the alternatives is needed for at least the LCM of their useful lives (or indefinitely).
2. **Identical Replacement:** The selected alternative will be replaced in each future cycle by an identical asset.
3. **Constant Cash Flows:** Cost estimates, salvage values, and annual receipts remain identical in every future cycle.

> ⚠️ **Note:** If cash flows or technologies change across future cycles, a fixed **study period analysis** must be used instead.
""")

st.markdown("---")

# Section 3: Capital Recovery and Annual Operating Cost
st.header("3. Capital Recovery (CR) and Annual Worth (AW)")

st.markdown("""
The net Annual Worth of any project consists of two core components:

$$
AW = CR + AOC
$$
""")

col_cr, col_aoc = st.columns(2)

with col_cr:
    st.subheader("Capital Recovery ($CR$)")
    st.markdown("""
    The equivalent annual amount an asset must earn to fully recover the initial capital investment ($P$, CapEx) plus the required return (MARR, $i$), accounting for terminal salvage value ($S$):

    $$
    CR = -P(A/P, i, n) + S(A/F, i, n)
    $$
    """)

with col_aoc:
    st.subheader("Annual Operating Cost ($AOC$)")
    st.markdown("""
    The equivalent uniform annual operating cash flow (OpEx), including maintenance, operational expenditures, or net operating revenues/savings.
    
    * For pure cost alternatives: $AOC < 0$.
    * For revenue alternatives: $AOC$ represents annual net operational profit/revenue.
    """)

st.markdown("---")

# Section 4: Decision Guidelines
st.header("4. Decision Guidelines")

st.markdown("""
| Alternative & Project Type | Criterion | Decision Rule |
| :--- | :--- | :--- |
| **Mutually Exclusive - Revenue** | Maximum Positive AW | Select alternative with $\\max AW_j \\ge 0$. If all $AW_j < 0$, select **Do-Nothing (DN)**. |
| **Mutually Exclusive - Cost** | Least Negative AW | Select alternative with $\\max AW_j$ (lowest equivalent annual cost). |
| **Independent Projects** | Absolute Feasibility | Accept **all** projects where $AW_k(i = \\text{MARR}) \\ge 0$. |
""")

st.markdown("---")

# Section 5: Permanent Investments
st.header("5. Annual Worth of Permanent Investments ($n = \\infty$)")

st.markdown("""
For public infrastructure, dams, highways, or university endowments ($n = \\infty$), Annual Worth is directly related to Capitalized Cost ($CC$):

$$
AW = CC \\times i
$$

### Component Conversions for Perpetuities:
* **Initial Capital Cost ($P$ at $t=0$):** $A_P = P \\cdot i$
* **Perpetual Annual Amount ($A$):** $A$ (no transformation needed)
* **Recurring Component ($R$ every $n_R$ years):** $A_R = R(A/F, i, n_R) = R \\left[ \\frac{i}{(1+i)^{n_R} - 1} \\right]$
* **Non-Recurring Component ($C$ at Year $n_C$):** $A_C = C(P/F, i, n_C) \\cdot i = \\frac{C \\cdot i}{(1+i)^{n_C}}$
""")

st.markdown("---")
st.header("📚 Formula Sheet")

st.markdown("""
| Name | Notation | Equation | Excel Function |
| :--- | :---: | :---: | :--- |
| **Annual Worth from PW** | $(A/P, i, n)$ | $AW = PW \\times \\left[ \\frac{i(1+i)^n}{(1+i)^n - 1} \\right]$ | `=PMT(i%, n, -PW)` |
| **Annual Worth from FW** | $(A/F, i, n)$ | $AW = FW \\times \\left[ \\frac{i}{(1+i)^n - 1} \\right]$ | `=PMT(i%, n, , -FW)` |
| **Capital Recovery** | $CR$ | $CR = -P(A/P,i,n) + S(A/F,i,n)$ | `=PMT(i%, n, P, -S)` |
| **Perpetual Initial Cost** | $A_P$ | $A_P = P \\cdot i$ | *N/A* |
| **Perpetual Recurring Cost** | $A_R$ | $A_R = R(A/F, i, n_R)$ | `=PMT(i%, n_R, , -R)` |
| **Perpetual Non-Recurring Cost**| $A_C$ | $A_C = C(P/F, i, n_C) \\cdot i$ | `=PV(i%, n_C, , -C) * i%` |
""")
