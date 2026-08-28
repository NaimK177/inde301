import streamlit as st

st.set_page_config(page_title="Ch5: Main Ideas & Formulas", layout="wide")

st.title("💡 Chapter 5: Present Worth & Economic Criteria")

st.markdown("""
This chapter establishes quantitative decision-making criteria for comparing and selecting economic alternatives using **Present Worth (PW)**, **Future Worth (FW)**, **Capitalized Cost (CC)**, **Payback Period**, and **Life-Cycle Cost (LCC)** techniques.
""")

st.markdown("---")

# Section 1: Alternatives & Project Classification
st.header("1. Classification of Alternatives & Projects")

st.markdown("""
Proposals undergo initial screening to eliminate non-feasible options. Viable proposals are called **alternatives**.
To evaluate alternatives economically, we classify them by **project interaction** and **cash flow structure**.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Types of Economic Projects")
    st.markdown("""
    | Project Type | Selection Constraint | Competing Against | Decision Rule |
    | :--- | :--- | :--- | :--- |
    | **Mutually Exclusive** | Select at most **ONE** alternative | Compete directly with each other | Select the single best alternative according to the criterion |
    | **Independent** | Select **MORE THAN ONE** alternative | Compete against Do-Nothing | Select **ALL** alternatives that meet or exceed MARR ($PW \\ge 0$) |
    """)

with col2:
    st.subheader("Types of Cash Flows")
    st.markdown("""
    | Cash Flow Type | Description | Economic Objective | Decision Criteria |
    | :--- | :--- | :--- | :--- |
    | **Revenue** | Generates both costs (outflows) and revenues/savings (inflows) | **Maximize Profit** | Select alternative with highest positive $PW(i = \\text{MARR})$ |
    | **Cost / Service** | Generates only cost estimates; revenues are equal or non-existent | **Minimize Cost** | Select alternative with least negative (highest) $PW(i = \\text{MARR})$ |
    """)

st.markdown("""
### The Do-Nothing (DN) Alternative
- **For Revenue Alternatives & Independent Projects:** Do-Nothing is always a feasible option. If no revenue alternative yields $PW \\ge 0$, DN is chosen.
- **For Cost / Service Alternatives:** Do-Nothing is typically **not** an option because the required service must be provided regardless.
""")

with st.expander("📌 Example Context: Baby Diaper Production Facility"):
    st.markdown("""
    A production line yields 200,000 diapers/day at 95% efficiency. To increase performance:
    - **Mutually Exclusive (Competing) Alternatives:**
      - **A (New Line):** $6M cost, generates +$5,000/day extra revenue (6-year life).
      - **B (Used Line):** $2.5M cost, generates +$2,000/day extra revenue (3-year life).
      - **C (Co-developed Line):** $5M cost, generates +$3,000/day extra revenue (4-year life).
    - **Independent Projects (Can select any combination):**
      - **Project 1:** Online inspection system ($100k cost, $2k annual subscription, $15k scrap savings).
      - **Project 2:** Guiding system replacement ($16k cost, $5k annual downtime savings).
      - **Project 3:** Carbide cutting die ($300k cost, $40k annual tooling savings).
    """)

st.markdown("---")

# Section 2: Present Worth Analysis
st.header("2. Present Worth (PW) Analysis")

st.markdown("""
**Present Worth (PW) Analysis** discounts all estimated cash inflows and outflows to a single base point in time ($t = 0$) at the Minimum Attractive Rate of Return (MARR, $i$).

$$
PW(i) = \\sum_{k=0}^{N} F_k (1+i)^{-k}
$$
""")

st.subheader("Decision Rules for Equal-Life Alternatives")
st.markdown("""
| Alternative & Project Type | Criterion | Decision Rule |
| :--- | :--- | :--- |
| **Mutually Exclusive - Revenue** | Highest Positive PW | Choose alternative with $\\max PW_j \\ge 0$. If all $PW_j < 0$, choose **Do-Nothing**. |
| **Mutually Exclusive - Cost** | Least Negative PW | Choose alternative with $\\max PW_j$ (lowest magnitude of cost). |
| **Independent Projects** | Absolute Feasibility | Accept **all** projects where $PW_k(i = \\text{MARR}) \\ge 0$. |
""")

st.markdown("---")

# Section 3: Equal-Service Requirement & Different-Life Alternatives
st.header("3. Equal-Service Requirement & Different-Life Alternatives")

st.info("""
**Equal-Service Requirement:** When comparing mutually exclusive alternatives, their Present Worth **must be evaluated over the same number of years** and end at the exact same point in time. 
Comparing cost alternatives over unequal lives without adjustment improperly favors shorter-lived options simply because fewer years of costs are accumulated.
""")

col_lcm, col_sp = st.columns(2)

with col_lcm:
    st.subheader("Method 1: Lowest Common Multiple (LCM)")
    st.markdown("""
    Evaluates alternatives over the **Lowest Common Multiple** of their useful lives.
    
    **Assumptions:**
    1. Service is needed for at least LCM years.
    2. Selected alternative is repeated over each life cycle in exactly the same manner.
    3. Cash flow estimates remain identical in every cycle (reinvesting initial cost $P$ at the start of each cycle, receiving salvage $S$ at the end of each cycle).
    """)

with col_sp:
    st.subheader("Method 2: Study Period Approach")
    st.markdown("""
    Evaluates all alternatives over a **fixed planning horizon ($n$)**, regardless of individual useful lives.
    
    | Case | Required Adjustment |
    | :--- | :--- |
    | **Life = Study Period** | No adjustment required. |
    | **Life > Study Period** | Estimate terminal market (or book) value at $t=n$ as a cash inflow. |
    | **Life < Study Period** | Do **not** replace asset. Compound all net cash flows at the end of useful life to $t=n$ at MARR. |
    """)

st.warning("""
⚠️ **Common Excel Trap: The `=NPV` Function**  
In Excel, passing the Year 0 cash flow inside `=NPV(rate, CF0:CFn)` incorrectly discounts Year 0 by 1 period!  
**Correct Excel Formula:** `PW = NPV(rate, CF1:CFn) + CF0`
""")

st.markdown("---")

# Section 4: Future Worth Analysis
st.header("4. Future Worth (FW) Analysis")

st.markdown("""
**Future Worth (FW) Analysis** compounds all cash flows to period $N$ at the MARR ($i$):

$$
FW(i) = \\sum_{k=0}^{N} F_k (1+i)^{N-k} = PW(i) \\times (1+i)^N
$$

**Equivalence:** PW and FW yield **identical ranking decisions**. FW is specifically useful when:
1. Primary goal is maximizing future stockholder wealth.
2. An asset is intended to be sold after a specific startup/holding period.
3. Projects take several years to build before generating returns (e.g. large infrastructure/construction).
""")

st.markdown("---")

# Section 5: Capitalized Cost Analysis
st.header("5. Capitalized Cost (CC) Analysis")

st.markdown("""
**Capitalized Cost (CC)** is the Present Worth of a project with an **infinite useful life** ($n \\to \\infty$), commonly applied to public infrastructure (bridges, dams, highways) or university endowments.

For a uniform perpetual annual series $A$:
$$
CC = \\lim_{n \\to \\infty} A \\left[ \\frac{1-(1+i)^{-n}}{i} \\right] = \\frac{A}{i}
$$

### General Procedure for Any Cash Flow Pattern:
1. **Non-Recurring Cash Flows ($P, F_k$):** Convert directly to Present Worth ($CC = PW$).
2. **Perpetual Annual Cash Flow ($A$):** $CC = A / i$.
3. **Recurring Component every $n_R$ years ($R$):** Convert to equivalent uniform annual worth over one cycle: $A_R = R(A/F, i, n_R)$, then $CC_R = A_R / i$.
4. **Finite vs. Infinite Comparison:** For a finite-life alternative ($n$), convert to annual worth $A = PW(A/P,i,n)$, then $CC_{\\text{finite}} = A / i$.
""")

st.markdown("---")

# Section 6: Payback Period Analysis
st.header("6. Payback Period Analysis")

st.markdown("""
The payback period $n_P$ is the estimated time required for cash inflows/savings to fully recover the initial investment $P$ plus return rate $i$:

$$
0 = -P + \\sum_{t=1}^{n_P} NCF_t (1+i)^{-t}
$$
""")

st.error("""
🚨 **Caution on Payback Period Analysis (The Payback Trap)**  
Payback analysis should **only** be used as a quick initial screening tool. It is flawed because:
1. **Ignores all cash flows after $n_P$**, missing major long-term revenues or salvage values.
2. **Neglects time value of money** when $i=0\\%$ payback is used.
""")

st.markdown("---")

# Section 7: Life-Cycle Cost Analysis
st.header("7. Life-Cycle Cost (LCC) Analysis")

st.markdown("""
Life-Cycle Costing evaluates total costs across all project phases: **Acquisition**, **Operation**, and **Phaseout / Disposal**.
""")

st.markdown("""
### Committed vs. Actual Costs

| Concept | Definition | Key Fact |
| :--- | :--- | :--- |
| **Committed Cost** | Cost locked in by early design, engineering, and architectural decisions | **75% to 85%** of total LCC is committed during preliminary & detailed design |
| **Actual Cost** | Physical disbursement and expenditure of funds | Actual spending trails committed spending |

> 💡 **Takeaway:** The greatest opportunity to minimize total LCC occurs during early design. Short-term cost cutting during acquisition often leads to massive operational failures and cost increases later.
""")
