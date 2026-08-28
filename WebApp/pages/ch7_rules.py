import streamlit as st

st.title("📜 Descartes vs Norstrom Rules")

st.header("Rules for Analyzing Cash Flows")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Descartes' Rule of Signs")
    st.info(
        "**Maximum Roots limit:**\n\n"
        "The **maximum number of roots** (Rates of Return) of a cash flow series is equal to the number of sign changes in the raw cash flows.\n\n"
        "*Example:* A cash flow with 3 sign changes can have at most 3 positive roots."
    )

with col2:
    st.subheader("Norstrom's Criterion")
    st.success(
        "**Guaranteeing a Unique Positive Root:**\n\n"
        "If the **cumulative cash flow** starts negatively and changes sign exactly once, there is guaranteed to be exactly **one unique positive root**.\n\n"
        "*Note:* This is a much stronger test than Descartes' rule. If Norstrom's criterion is satisfied, you don't need to worry about multiple roots!"
    )

st.divider()
st.header("Cash Flow Analyzer")
st.markdown("Edit the cash flows below to automatically count the sign changes and evaluate both rules. The table is synced with the Solver tab!")

import pandas as pd
import numpy as np

if 'cf_data' not in st.session_state or "Year" in st.session_state['cf_data'].columns:
    df = pd.DataFrame({
        "Cash Flow ($)": [-100000.0, 30000.0, 30000.0, 30000.0, 30000.0, 30000.0]
    })
    df.index.name = "Year"
    st.session_state['cf_data'] = df

edited_df = st.data_editor(
    st.session_state['cf_data'],
    num_rows="dynamic",
    use_container_width=True,
)
# Convert index back to Year column for processing and breakdown table
edited_df = edited_df.reset_index()

if not edited_df.empty:
    flows = edited_df["Cash Flow ($)"].tolist()
    
    # Calculate Descartes sign changes
    descartes_changes = 0
    prev_sign = None
    for f in flows:
        if f == 0: continue
        sign = 1 if f > 0 else -1
        if prev_sign is not None and sign != prev_sign:
            descartes_changes += 1
        prev_sign = sign
        
    # Calculate Cumulative Cash Flows (S_t)
    cum_flows = np.cumsum(flows).tolist()
    
    # Calculate Norstrom sign changes
    norstrom_changes = 0
    prev_cum_sign = None
    for cf in cum_flows:
        if cf == 0: continue
        sign = 1 if cf > 0 else -1
        if prev_cum_sign is not None and sign != prev_cum_sign:
            norstrom_changes += 1
        prev_cum_sign = sign
        
    st.subheader("Analysis Results")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Descartes Sign Changes", descartes_changes)
        if descartes_changes <= 1:
            st.success(f"✅ **Conventional Cash Flow:** Descartes' rule guarantees a maximum of {max(0, descartes_changes)} positive root.")
        else:
            st.warning(f"⚠️ **Unconventional Cash Flow:** Descartes' rule allows up to {descartes_changes} positive roots.")
            
    with col_res2:
        st.metric("Norstrom Sign Changes", norstrom_changes)
        if flows[0] < 0 and norstrom_changes == 1:
            st.success("✅ **Norstrom's Criterion Satisfied:** $S_0 < 0$ and exactly 1 sign change. There is exactly one unique positive root.")
        else:
            reason = []
            if flows[0] >= 0:
                reason.append("Starts positively ($S_0 \\ge 0$)")
            if norstrom_changes != 1:
                reason.append(f"Has {norstrom_changes} sign changes")
            st.error(f"❌ **Norstrom's Criterion Fails:** {', '.join(reason)}. Does not guarantee a unique positive root.")
            
    st.write("### Detailed Breakdown")
    analysis_df = edited_df.copy()
    analysis_df["Cumulative Cash Flow ($S_t$)"] = cum_flows
    st.dataframe(analysis_df, hide_index=True, use_container_width=True)
