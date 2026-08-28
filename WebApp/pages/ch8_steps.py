import streamlit as st

st.title("📋 Step-by-Step Analysis Guide")

st.markdown(r"""
This guide outlines the exact algorithm to perform Incremental Rate of Return (ROR) analysis. 

The procedure differs slightly depending on whether you are comparing exactly two mutually exclusive alternatives or more than two.

---

### 1. Comparing Exactly Two Alternatives

When comparing two mutually exclusive alternatives, follow these steps:

1. **Order by Cost:** Order the alternatives by increasing first cost (initial investment). Let's call the one with the lower initial cost **Alternative A** and the higher initial cost **Alternative B**.
2. **Screening (Revenue Alternatives Only):** Compute the individual $i^*$ for each alternative. Any alternative with $i^* < MARR$ is eliminated. *(For cost-only alternatives, skip this step).*
3. **Equal-Service Requirement:** If the alternatives have unequal lives, expand their cash flows to the Lowest Common Multiple (LCM) of their lives.
4. **Incremental Cash Flow:** Calculate the incremental cash flow series: 
   $$ \Delta CF_t = CF_{B,t} - CF_{A,t} $$
5. **Incremental ROR:** Determine the incremental rate of return $\Delta i^*_{B-A}$ by setting the Present Worth of the incremental series to 0:
   $$ PW_{\Delta}(\Delta i^*) = 0 $$
6. **Decision:** 
   - If $\Delta i^*_{B-A} \geq MARR$, select the higher-cost alternative (**Select B**).
   - If $\Delta i^*_{B-A} < MARR$, select the lower-cost alternative (**Select A**).

---

### 2. Comparing Multiple (More Than Two) Alternatives

When more than two mutually exclusive alternatives exist, the incremental ROR method is executed as a "tournament" of successive pairwise comparisons:

1. **Rank by Cost:** Rank all alternatives from **smallest to largest** initial investment.
2. **Initial Screening (Revenue Alternatives Only):** Compute $i^*$ for each alternative. Discard any alternative with $i^* < MARR$.
   - *Note: If all revenue alternatives are discarded, select the **"Do Nothing"** alternative.*
3. **First Matchup:** Set the first surviving alternative as the **Defender** and the next surviving alternative as the **Challenger**.
4. **Pairwise Comparison:** Compute the incremental cash flow between the Challenger and the Defender (using the LCM if their lives differ) and determine $\Delta i^*$.
5. **Determine the Winner:**
   - If $\Delta i^* \geq MARR$, the **Challenger wins** and becomes the new Defender.
   - If $\Delta i^* < MARR$, the **current Defender survives**.
6. **Iterate:** Repeat Steps 4 and 5 by pitting the winner against the next alternative in the ranked list until all alternatives have been evaluated. The final surviving alternative is the best option.
""")
