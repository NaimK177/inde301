import streamlit as st

st.title("💡 Chapter 7: Main Ideas & Formulas")

st.markdown(r"""
### Rate of Return (ROR)
The **Rate of Return ($i^*$)** is the interest rate that brings the Present Worth (PW), Annual Worth (AW), or Future Worth (FW) of a cash flow series to exactly zero.

$$PW(i^*) = 0 \quad \text{or} \quad AW(i^*) = 0 \quad \text{or} \quad FW(i^*) = 0$$

The most common way to solve for $i^*$ is by using the Present Worth equation:

$$ \sum_{t=0}^{n} F_t (1+i^*)^{-t} = 0 $$

where $F_t$ is the net cash flow at time $t$.

---
### Conventional vs. Unconventional Cash Flows
- **Conventional Cash Flow:** The cash flow changes sign exactly once (usually from negative to positive). These are mathematically guaranteed to have a unique positive $i^*$.
- **Unconventional Cash Flow:** The cash flow changes sign more than once. These can yield multiple $i^*$ values, making standard analysis ambiguous without assuming a reinvestment rate.

---
### Pros and Cons of ROR
**Advantages:**
- Does not require estimating a Minimum Attractive Rate of Return (MARR) beforehand.
- The percentage format is highly intuitive and favored by management and investors.

**Disadvantages:**
- Computationally difficult to solve by hand (trial and error).
- Can yield multiple roots for unconventional cash flows.
- Requires a specialized incremental procedure when comparing multiple mutually exclusive alternatives.
""")
