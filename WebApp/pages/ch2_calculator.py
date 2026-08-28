import sys
import os
import streamlit as st

# Add the Codes directory to the path so we can import factors from ch2
current_dir = os.path.dirname(os.path.abspath(__file__))
webapp_dir = os.path.abspath(os.path.join(current_dir, '..'))
codes_dir = os.path.abspath(os.path.join(webapp_dir, '..'))
if codes_dir not in sys.path:
    sys.path.append(codes_dir)

from ch2 import factors

st.set_page_config(page_title="Ch2: Calculator", layout="wide")

st.title("📈 Interactive Calculator")
st.markdown("Easily compute standard engineering economy factors and visualize amortization schedules.")

# --- Calculator Inputs ---
st.header("Input Parameters")

factor_choice = st.selectbox(
    "Select Factor",
    [
        "Find F given P (F/P)",
        "Find P given F (P/F)",
        "Find P given A (P/A)",
        "Find F given A (F/A)",
        "Find A given P (A/P) - Capital Recovery",
        "Find A given F (A/F) - Sinking Fund",
        "Find P given G (P/G) - Arithmetic Gradient",
        "Find A given G (A/G) - Arithmetic Gradient",
        "Find P given g (P_g) - Geometric Gradient"
    ]
)

is_gradient = "(P/G)" in factor_choice or "(A/G)" in factor_choice
is_geometric = "(P_g)" in factor_choice

if is_gradient:
    base_amount = st.number_input("Uniform Base Amount (A)", value=1000.0, step=100.0)
    gradient_amount = st.number_input("Gradient Amount (G)", value=200.0, step=50.0)
elif is_geometric:
    base_amount = st.number_input("Initial Amount (A_1)", value=1000.0, step=100.0)
    growth_rate_pct = st.number_input("Growth Rate g (%)", value=10.0, step=0.1)
else:
    # Determine the label for the base amount based on the selection
    base_amount_label = "Base Amount"
    if "(F/P)" in factor_choice or "(A/P)" in factor_choice:
        base_amount_label = "Present Worth (P)"
    elif "(P/F)" in factor_choice or "(A/F)" in factor_choice:
        base_amount_label = "Future Worth (F)"
    elif "(P/A)" in factor_choice or "(F/A)" in factor_choice:
        base_amount_label = "Uniform Series Amount (A)"
    
    base_amount = st.number_input(f"{base_amount_label}", value=1000.0, step=100.0)

interest_rate_pct = st.number_input("Interest Rate (%)", value=5.0, step=0.1)
periods = st.number_input("Number of Periods (n)", value=10, min_value=1, step=1)

calculate_btn = st.button("Calculate")

st.markdown("---")

# --- Results & Formulas ---
st.header("Mathematical Formula")

if "(F/P)" in factor_choice:
    st.latex(r"F = P(1+i)^n")
elif "(P/F)" in factor_choice:
    st.latex(r"P = \frac{F}{(1+i)^n} = F(1+i)^{-n}")
elif "(P/A)" in factor_choice:
    st.latex(r"P = A \left[ \frac{(1+i)^n - 1}{i(1+i)^n} \right]")
elif "(F/A)" in factor_choice:
    st.latex(r"F = A \left[ \frac{(1+i)^n - 1}{i} \right]")
elif "(A/P)" in factor_choice:
    st.latex(r"A = P \left[ \frac{i(1+i)^n}{(1+i)^n - 1} \right]")
elif "(A/F)" in factor_choice:
    st.latex(r"A = F \left[ \frac{i}{(1+i)^n - 1} \right]")
elif "(P/G)" in factor_choice:
    st.latex(r"P_{total} = A \left[ \frac{(1+i)^n - 1}{i(1+i)^n} \right] + G \left[ \frac{(1+i)^n - in - 1}{i^2(1+i)^n} \right]")
elif "(A/G)" in factor_choice:
    st.latex(r"A_{total} = A + G \left[ \frac{1}{i} - \frac{n}{(1+i)^n - 1} \right]")
elif "(P_g)" in factor_choice:
    st.latex(r"P_g = A_1 \left[ \frac{\left(\frac{1+g}{1+i}\right)^n - 1}{g - i} \right] \quad (i \neq g)")
    st.latex(r"P_g = \frac{n A_1}{1+i} \quad (i = g)")

st.markdown("---")

if calculate_btn:
    i = interest_rate_pct / 100.0
    n = int(periods)
    
    result = 0.0
    
    # Map the choice to the correct function
    if "(F/P)" in factor_choice:
        result = factors.calculate_fp(i, n, p=base_amount)
    elif "(P/F)" in factor_choice:
        result = factors.calculate_pf(i, n, f=base_amount)
    elif "(P/A)" in factor_choice:
        result = factors.calculate_pa(i, n, a=base_amount)
    elif "(F/A)" in factor_choice:
        result = factors.calculate_fa(i, n, a=base_amount)
    elif "(A/P)" in factor_choice:
        result = factors.calculate_ap(i, n, p=base_amount)
    elif "(A/F)" in factor_choice:
        result = factors.calculate_af(i, n, f=base_amount)
    elif "(P/G)" in factor_choice:
        result = factors.calculate_composite_pg(i, n, a=base_amount, g=gradient_amount)
    elif "(A/G)" in factor_choice:
        result = factors.calculate_composite_ag(i, n, a=base_amount, g=gradient_amount)
    elif "(P_g)" in factor_choice:
        g_rate = growth_rate_pct / 100.0
        result = factors.calculate_geometric_pg(i, n, a1=base_amount, g=g_rate)
        
    st.success(f"### Calculated Result: **${result:,.2f}**")
    
    # Generate Cash Flow Diagram Array
    amounts = [0.0] * (n + 1)
    if "(F/P)" in factor_choice:
        amounts[0] = -base_amount
        amounts[n] = result
    elif "(P/F)" in factor_choice:
        amounts[0] = -result
        amounts[n] = base_amount
    elif "(P/A)" in factor_choice:
        amounts[0] = -result
        for t in range(1, n + 1):
            amounts[t] = base_amount
    elif "(F/A)" in factor_choice:
        for t in range(1, n + 1):
            amounts[t] = -base_amount
        amounts[n] += result
    elif "(A/P)" in factor_choice:
        amounts[0] = base_amount
        for t in range(1, n + 1):
            amounts[t] = -result
    elif "(A/F)" in factor_choice:
        for t in range(1, n + 1):
            amounts[t] = -result
        amounts[n] += base_amount
    elif "(P/G)" in factor_choice:
        amounts[0] = -result
        for t in range(1, n + 1):
            amounts[t] = base_amount + (t - 1) * gradient_amount
    elif "(A/G)" in factor_choice:
        p_total = factors.calculate_composite_pg(i, n, a=base_amount, g=gradient_amount)
        amounts[0] = -p_total
        for t in range(1, n + 1):
            amounts[t] = base_amount + (t - 1) * gradient_amount
    elif "(P_g)" in factor_choice:
        amounts[0] = -result
        g_rate = growth_rate_pct / 100.0
        for t in range(1, n + 1):
            amounts[t] = base_amount * (1 + g_rate)**(t - 1)

    st.markdown("---")
    st.subheader("📈 Cash Flow Diagram")
    cf_fig = factors.plot_cash_flow(list(range(n + 1)), amounts)
    st.plotly_chart(cf_fig, width='stretch')
    

