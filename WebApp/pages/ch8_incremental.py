import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as plotly_go
import math

st.title("⚖️ Incremental ROR Solver")

st.markdown("""
This tool evaluates two mutually exclusive alternatives using the **Incremental Rate of Return** method.
Enter the cash flows for both alternatives. If they have unequal lives, use the **Expand to LCM** button to satisfy the equal-service requirement before comparing.
""")

col_marr, _ = st.columns(2)
with col_marr:
    marr = st.number_input("Minimum Attractive Rate of Return (MARR) %", value=10.0, step=0.5) / 100.0

st.subheader("1. Enter Cash Flows")

# Setup initial dataframe
if 'ch8_cf_data_a' not in st.session_state:
    st.session_state['ch8_cf_data_a'] = pd.DataFrame({"Year": [0, 1, 2, 3], "Cash Flow ($)": [-8000.0, 6000.0, 6000.0, 7000.0]})
if 'ch8_cf_data_b' not in st.session_state:
    st.session_state['ch8_cf_data_b'] = pd.DataFrame({"Year": [0, 1, 2, 3, 4, 5, 6], "Cash Flow ($)": [-20000.0, 7000.0, 7000.0, 7000.0, 7000.0, 7000.0, 10000.0]})

col1, col2 = st.columns(2)

with col1:
    st.write("**Alternative 1**")
    edited_df_a = st.data_editor(
        st.session_state['ch8_cf_data_a'],
        num_rows="dynamic",
        key="editor_a",
        use_container_width=True,
    )

with col2:
    st.write("**Alternative 2**")
    edited_df_b = st.data_editor(
        st.session_state['ch8_cf_data_b'],
        num_rows="dynamic",
        key="editor_b",
        use_container_width=True,
    )

def extract_array(df):
    if df.empty: return []
    df_sorted = df.sort_values("Year")
    max_year = int(df_sorted["Year"].max())
    arr = np.zeros(max_year + 1)
    for _, row in df_sorted.iterrows():
        y = row["Year"]
        f = row["Cash Flow ($)"]
        if y >= 0 and y == int(y):
            arr[int(y)] = f
    return arr

arr_1 = extract_array(edited_df_a)
arr_2 = extract_array(edited_df_b)

len_1 = len(arr_1) - 1 if len(arr_1) > 0 else 0
len_2 = len(arr_2) - 1 if len(arr_2) > 0 else 0

st.subheader("2. Equal-Service Requirement")

if len_1 != len_2 and len_1 > 0 and len_2 > 0:
    st.warning(f"The alternatives have different lives ({len_1} years vs {len_2} years). You must evaluate them over an equal-service period.")
    if st.button("Expand to LCM", type="primary"):
        lcm = math.lcm(len_1, len_2)
        
        # Expand 1
        new_arr_1 = np.zeros(lcm + 1)
        for cycle in range(lcm // len_1):
            offset = cycle * len_1
            for y, val in enumerate(arr_1):
                new_arr_1[offset + y] += val
        
        # Expand 2
        new_arr_2 = np.zeros(lcm + 1)
        for cycle in range(lcm // len_2):
            offset = cycle * len_2
            for y, val in enumerate(arr_2):
                new_arr_2[offset + y] += val
                
        # Update session state and rerun
        st.session_state['ch8_cf_data_a'] = pd.DataFrame({"Year": np.arange(lcm + 1), "Cash Flow ($)": new_arr_1})
        st.session_state['ch8_cf_data_b'] = pd.DataFrame({"Year": np.arange(lcm + 1), "Cash Flow ($)": new_arr_2})
        st.rerun()
elif len_1 > 0 and len_1 == len_2:
    st.success(f"Both alternatives have an equal study period of {len_1} years.")

st.divider()

if len_1 == len_2 and len_1 > 0:
    st.subheader("3. Incremental Analysis")
    
    # Identify which is higher initial cost (B)
    cost_1 = -arr_1[0] if arr_1[0] < 0 else 0
    cost_2 = -arr_2[0] if arr_2[0] < 0 else 0
    
    if cost_1 > cost_2:
        arr_b = arr_1
        arr_a = arr_2
        name_b = "Alternative 1"
        name_a = "Alternative 2"
    else:
        arr_b = arr_2
        arr_a = arr_1
        name_b = "Alternative 2"
        name_a = "Alternative 1"
        
    st.write(f"**{name_b}** has the higher initial investment and is designated as **Alternative B**.")
    st.write(f"**{name_a}** is designated as **Alternative A**.")
    
    arr_diff = arr_b - arr_a
    
    df_diff = pd.DataFrame({
        "Year": np.arange(len(arr_diff)),
        f"{name_a} (A)": arr_a,
        f"{name_b} (B)": arr_b,
        "Incremental (B - A)": arr_diff
    })
    st.dataframe(df_diff, use_container_width=True, hide_index=True)
    
    def find_roots(cf_array):
        # We need a continuous array of cash flows for np.roots
        coeffs = cf_array[::-1] 
        roots = np.roots(coeffs)
        real_roots = roots[(np.isreal(roots)) & (roots > 0)].real
        rates = (1 / real_roots) - 1
        return np.sort(np.unique(np.round(rates, 6)))
        
    roots_diff = find_roots(arr_diff)
    
    if len(roots_diff) == 0:
        st.error("No valid Incremental Rate of Return found.")
    else:
        delta_i = roots_diff[0] 
        if len(roots_diff) > 1:
            st.warning(f"Multiple incremental RORs found: {', '.join([f'{r*100:.2f}%' for r in roots_diff])}. Using {delta_i*100:.2f}%.")
            
        st.info(f"**Incremental Rate of Return ($\\Delta i^*$): {delta_i*100:.2f}%**")
        
        if delta_i >= marr:
            st.success(f"Since $\\Delta i^* \\ge \\text{{MARR}}$ ({delta_i*100:.2f}% $\\ge$ {marr*100:.2f}%), **Select {name_b}** (the higher-investment alternative).")
        else:
            st.success(f"Since $\\Delta i^* < \\text{{MARR}}$ ({delta_i*100:.2f}% $<$ {marr*100:.2f}%), the extra investment is not justified. **Select {name_a}**.")

    st.subheader("4. Present Worth Comparison")
    
    # Plot PW curves
    i_values = np.linspace(-0.2, 0.5, 500)
    if delta_i > 0.4:
        i_values = np.linspace(-0.2, delta_i + 0.2, 500)
        
    pw_a = [sum(f / ((1 + i)**t) for t, f in enumerate(arr_a)) for i in i_values]
    pw_b = [sum(f / ((1 + i)**t) for t, f in enumerate(arr_b)) for i in i_values]
    
    fig = plotly_go.Figure()
    fig.add_trace(plotly_go.Scatter(x=i_values*100, y=pw_a, mode='lines', name=f'PW of {name_a}'))
    fig.add_trace(plotly_go.Scatter(x=i_values*100, y=pw_b, mode='lines', name=f'PW of {name_b}'))
    
    # Add vertical line for delta i
    fig.add_vline(x=delta_i*100, line_dash="dash", line_color="green", annotation_text=f"Δi* = {delta_i*100:.2f}%")
    # Add vertical line for MARR
    fig.add_vline(x=marr*100, line_dash="dot", line_color="red", annotation_text=f"MARR = {marr*100:.2f}%")
    
    fig.update_layout(
        xaxis_title="Interest Rate i (%)",
        yaxis_title="Present Worth ($)",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
