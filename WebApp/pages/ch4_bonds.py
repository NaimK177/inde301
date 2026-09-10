import sys
import os
import streamlit as st

# Add the Codes directory to the path so we can import from ch4 and ch2
current_dir = os.path.dirname(os.path.abspath(__file__))
webapp_dir = os.path.abspath(os.path.join(current_dir, '..'))
codes_dir = os.path.abspath(os.path.join(webapp_dir, 'Codes'))
if codes_dir not in sys.path:
    sys.path.append(codes_dir)

from ch4.pricetoyield import plot_bond_price_vs_yield
from ch2.factors import plot_cash_flow

st.set_page_config(page_title="Ch4: Bond Calculator", layout="wide")

st.title("💵 Bond Calculator")
st.markdown("Calculate the Present Value (Purchase Price) of a bond, visualize its cash flow, and see how the price relates to the Yield to Maturity.")

# --- Bond Parameters ---
st.header("Bond Parameters")

F = st.number_input("Face Value ($)", min_value=100.0, value=1000.0, step=100.0)

coupon_input_type = st.radio("Coupon Input Type", ["Coupon Value ($)", "Coupon Rate (%)"])
if coupon_input_type == "Coupon Value ($)":
    C = st.number_input("Total Annual Coupon ($)", min_value=0.0, value=100.0, step=10.0)
    coupon_rate = None
else:
    C = None
    coupon_rate_pct = st.number_input("Annual Coupon Rate (%)", min_value=0.0, value=10.0, step=0.5)
    coupon_rate = coupon_rate_pct / 100.0

m = st.selectbox(
    "Compounding Periods per Year (m)", 
    options=[1, 2, 4, 12], 
    index=1, 
    format_func=lambda x: f"{x} ({'Annual' if x==1 else 'Semi-annual' if x==2 else 'Quarterly' if x==4 else 'Monthly'})"
)
years = st.number_input("Years to Maturity", min_value=1, value=10, step=1)

st.markdown("---")
st.header("Market Conditions")
yield_pct = st.number_input("Yield to Maturity (%)", min_value=0.01, value=10.0, step=0.5)
yld = yield_pct / 100.0

calculate_btn = st.button("Calculate & Visualize")

# Resolve actual coupon value if rate was provided
if C is None:
    C_actual = F * coupon_rate
else:
    C_actual = C

n = years * m

if calculate_btn or True: # Always calculate based on current input
    # 1. Present Value Calculation
    # P = F*(1 + lambda/m)^(-n) + (C/lambda) * (1 - (1 + lambda/m)^(-n))
    discount_factor = (1 + yld / m)**(-n)
    pv_face = F * discount_factor
    pv_coupons = (C_actual / yld) * (1 - discount_factor)
    P = pv_face + pv_coupons

    st.markdown("---")
    st.header("1. Present Value (Purchase Price)")
    st.write(f"The fair purchase price of this bond today, to achieve a **{yield_pct}%** yield to maturity, is:")
    st.success(f"**${P:,.2f}**")
    
    st.markdown("---")
    st.header("2. Cash Flow Diagram (Investor's Perspective)")
    st.markdown("This represents the initial outflow (purchase price) and the subsequent inflows (coupons and face value at maturity).")
    
    # Generate Cash Flow Diagram Array
    periods = list(range(n + 1))
    amounts = []
    for i in periods:
        if i == 0:
            amounts.append(-P)
        elif i == n:
            amounts.append((C_actual / m) + F)
        else:
            amounts.append(C_actual / m)
    
    cf_fig = plot_cash_flow(periods=periods, amounts=amounts, title="Bond Cash Flow Diagram")
    st.plotly_chart(cf_fig, use_container_width=True)

    st.markdown("---")
    st.header("3. Bond Price vs. Yield Curve")
    
    # Generate Plot using existing function
    fig = plot_bond_price_vs_yield(F=F, C=C, coupon_rate=coupon_rate, m=m, years=years)
    
    # Add a point for the current user-selected yield
    fig.add_trace(dict(
        type='scatter',
        x=[yield_pct],
        y=[P],
        mode='markers',
        marker=dict(color='blue', size=12, symbol='star'),
        name=f'Current Yield ({yield_pct}%, ${P:,.2f})'
    ))

    st.plotly_chart(fig, use_container_width=True)
