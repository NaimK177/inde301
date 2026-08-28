import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as plotly_go

st.title("🧮 Rate of Return Solver")

st.markdown("""
This tool solves for the Rate of Return ($i^*$) by finding the interest rate that brings the Present Worth of the cash flow to exactly zero.

$$PW(i^*) = 0$$

You can use the interactive table below to input your cash flows. Add or remove rows to handle both simple and complex cash flows.
""")
    
# Setup initial dataframe
if 'cf_data' not in st.session_state or "Year" in st.session_state['cf_data'].columns:
    # Default simple cash flow: initial cost and 5 years of returns
    df = pd.DataFrame({
        "Cash Flow ($)": [-100000.0, 30000.0, 30000.0, 30000.0, 30000.0, 30000.0]
    })
    df.index.name = "Year"
    st.session_state['cf_data'] = df
    
st.subheader("1. Enter Cash Flows")

col_table, col_plot = st.columns([1, 2])

with col_table:
    edited_df = st.data_editor(
        st.session_state['cf_data'],
        num_rows="dynamic",
        use_container_width=True,
    )
    # Convert index back to Year column for processing
    edited_df = edited_df.reset_index()

with col_plot:
    # Dynamic Cashflow Diagram
    if not edited_df.empty:
        fig_cf = plotly_go.Figure()
        
        years = edited_df["Year"].tolist()
        flows = edited_df["Cash Flow ($)"].tolist()
        
        colors = ['green' if f >= 0 else 'red' for f in flows]
        
        fig_cf.add_trace(plotly_go.Bar(
            x=years,
            y=flows,
            marker_color=colors,
            text=[f"${f:,.0f}" for f in flows],
            textposition='auto',
        ))
        
        fig_cf.update_layout(
            title="Cash Flow Diagram",
            xaxis_title="Year (k)",
            yaxis_title="Amount ($)",
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_cf, use_container_width=True)

st.divider()
st.subheader("2. Results: Rate of Return & PW(i) Curve")

# Root finding logic
if not edited_df.empty and len(edited_df) > 1:
    years = edited_df["Year"].tolist()
    flows = edited_df["Cash Flow ($)"].tolist()
    
    # We need a continuous array of cash flows for np.roots
    max_year = int(max(years))
    cf_array = np.zeros(max_year + 1)
    for y, f in zip(years, flows):
        if y >= 0 and y == int(y): # ensure valid year
            cf_array[int(y)] = f
            
    # np.roots expects polynomial coefficients from highest degree to lowest
    # F_0 + F_1 x + F_2 x^2 ... + F_n x^n = 0
    # So highest degree is x^n, coefficient is F_n
    coeffs = cf_array[::-1] 
    
    roots = np.roots(coeffs)
    
    # Filter for real roots, where x > 0 (meaning i > -1)
    real_roots = roots[(np.isreal(roots)) & (roots > 0)].real
    
    # Convert x back to i: x = 1/(1+i) => i = (1/x) - 1
    rates_of_return = (1 / real_roots) - 1
    
    # Sort and remove near duplicates
    rates_of_return = np.sort(np.unique(np.round(rates_of_return, 6)))
    
    if len(rates_of_return) == 0:
        st.warning("No mathematically valid Rate of Return found (i > -100%).")
    elif len(rates_of_return) == 1:
        st.success(f"**Unique Rate of Return found:** {rates_of_return[0]*100:.2f}%")
    else:
        st.error(f"**MULTIPLE ROOTS DETECTED!** \n\nFound {len(rates_of_return)} valid Rates of Return: " + 
                 ", ".join([f"{r*100:.2f}%" for r in rates_of_return]))
        st.info("When multiple roots exist, the standard ROR method is ambiguous. Consider using an External Rate of Return (ERR) or Modified Internal Rate of Return (MIRR) method instead.")

    # Draw PW(i) curve
    # Determine range for plot
    min_rate = -0.5
    max_rate = 1.0
    if len(rates_of_return) > 0:
        max_rate = max(1.0, max(rates_of_return) + 0.5)
        min_rate = min(-0.5, min(rates_of_return) - 0.2)
        # prevent plotting below -100%
        min_rate = max(-0.99, min_rate)
        
    i_values = np.linspace(min_rate, max_rate, 500)
    pw_values = []
    for i in i_values:
        pw = sum(f / ((1 + i)**t) for t, f in enumerate(cf_array))
        pw_values.append(pw)
        
    fig_pw = plotly_go.Figure()
    fig_pw.add_trace(plotly_go.Scatter(
        x=i_values * 100,
        y=pw_values,
        mode='lines',
        name='PW(i)',
        line=dict(color='blue', width=2)
    ))
    
    # Add zero line
    fig_pw.add_hline(y=0, line_dash="dash", line_color="gray")
    
    # Mark roots
    for r in rates_of_return:
        fig_pw.add_trace(plotly_go.Scatter(
            x=[r * 100],
            y=[0],
            mode='markers',
            marker=dict(color='red', size=10, symbol='x'),
            name=f'Root: {r*100:.2f}%'
        ))

    fig_pw.update_layout(
        title="Present Worth vs. Interest Rate",
        xaxis_title="Interest Rate i (%)",
        yaxis_title="Present Worth ($)",
        template="plotly_white",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_pw, use_container_width=True)
