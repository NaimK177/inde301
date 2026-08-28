import streamlit as st

st.title("💡 Main Ideas & Formulas (Chapter 8)")

st.markdown(r"""
### Rate of Return Analysis: Multiple Alternatives

When evaluating mutually exclusive alternatives, comparing the individual Rate of Return ($i^*$) of each option is **not sufficient**. An alternative might have a high $i^*$ but generate very little total value due to a small initial investment. 

To properly compare alternatives on the basis of ROR, we must perform an **Incremental Analysis**.

#### The Incremental Cash Flow
The incremental cash flow ($\Delta CF$) represents the extra investment or cost required if the alternative with the larger first cost is selected. 

For two alternatives $A$ and $B$, where $B$ has the **higher initial investment**:
$$ \Delta CF_t = CF_{B,t} - CF_{A,t} $$

#### The Equal-Service Requirement
The incremental ROR method strictly requires that the alternatives be evaluated over an **equal-service study period**. If the alternatives have unequal lives, their cash flows must first be expanded to the **Lowest Common Multiple (LCM)** of their lives.

#### Incremental ROR ($\Delta i^*$)
Once the incremental cash flow series is found, we solve for the incremental rate of return ($\Delta i^*_{B-A}$):
$$ PW_{\Delta}(\Delta i^*) = 0 $$

#### The Decision Rule
Compare the incremental rate of return to the Minimum Attractive Rate of Return (MARR):
* If $\Delta i^*_{B-A} \geq MARR \rightarrow$ **Select B** (the extra investment is justified).
* If $\Delta i^*_{B-A} < MARR \rightarrow$ **Select A** (the extra investment is NOT justified).

#### The "Do Nothing" Baseline
For revenue alternatives, the "Do Nothing" (DN) alternative is implicitly the first defender with an initial cost of $0. If all individual ROR values fall below the MARR, all alternatives lose to DN, and no investment should be made.
""")
