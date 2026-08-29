import sys
import os
import streamlit as st

# Add the Codes directory to the path so we can import factors from ch2
current_dir = os.path.dirname(os.path.abspath(__file__))
webapp_dir = os.path.abspath(os.path.join(current_dir, '..'))
codes_dir = os.path.abspath(os.path.join(webapp_dir, 'Codes'))
if codes_dir not in sys.path:
    sys.path.append(codes_dir)

from ch2 import factors

st.set_page_config(page_title="Ch2: Amortization Schedule", layout="wide")

st.title("📊 Amortization Schedule")
st.markdown("Generate a detailed breakdown of your loan or investment over time.")

# --- Input Parameters ---
st.header("Input Parameters")

principal = st.number_input("Principal Amount (P)", value=10000.0, step=1000.0)
interest_rate_pct = st.number_input("Interest Rate (%)", value=5.0, step=0.1)
periods = st.number_input("Number of Periods (n)", value=10, min_value=1, step=1)

calculate_btn = st.button("Generate Schedule")
if calculate_btn:
    i = interest_rate_pct / 100.0
    n = int(periods)
    
    st.markdown("---")
    st.subheader("Amortization Breakdown")
    
    # Generate and display the DataFrame
    df_schedule = factors.generate_amortization_schedule(principal, i, n)
    
    # Calculate payment for cash flow diagram
    payment = factors.calculate_ap(i, n, p=principal)
    amounts = [principal] + [-payment] * n
    
    # Use columns to lay out the table and chart side-by-side
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.dataframe(df_schedule, width='stretch', hide_index=True)
        
    with col2:
        fig = factors.plot_amortization_breakdown(df_schedule)
        st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.subheader("📈 Cash Flow Diagram")
    cf_fig = factors.plot_cash_flow(list(range(n + 1)), amounts)
    st.plotly_chart(cf_fig, width='stretch')
