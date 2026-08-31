import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(page_title="Ch1: Calculator", layout="wide")

st.title("🧮 Chapter 1 Tools")
st.markdown("Interactive tools to understand the Rule of 72 and the impact of compounding.")

# --- Tool Selection ---
st.header("Select Tool")
tool_choice = st.radio("Tool", ["Rule of 72 Estimator", "Simple vs. Compound Interest"])

if tool_choice == "Rule of 72 Estimator":
    st.header("⏱️ Rule of 72 Estimator")
    st.markdown("Quickly estimate how long it takes for an investment to **double** in value.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        interest_rate = st.number_input("Annual Interest Rate (%)", value=9.0, step=0.5, min_value=0.1)
    
    years_approx = 72.0 / interest_rate
    
    # Calculate exact for comparison
    import math
    years_exact = math.log(2) / math.log(1 + (interest_rate / 100.0))
    
    st.success(f"### Estimated time to double: **{years_approx:,.1f} years**")
    st.info(f"*(For reference, the exact mathematical time is {years_exact:,.2f} years. The Rule of 72 is a very close mental-math approximation!)*")

elif tool_choice == "Simple vs. Compound Interest":
    st.header("📈 Simple vs. Compound Interest")
    st.markdown("Visualize the difference between simple interest (linear) and compound interest (exponential).")
    
    st.header("Input Parameters")
    principal = st.number_input("Principal Amount ($)", value=100000.0, step=5000.0)
    simple_rate = st.number_input("Simple Interest Rate (%)", value=8.5, step=0.1)
    compound_rate = st.number_input("Compound Interest Rate (%)", value=6.0, step=0.1)
    periods = st.slider("Number of Periods (Years)", min_value=1, max_value=50, value=20)
    
    # Calculate arrays
    n = np.arange(0, periods + 1, 1)
    simple_interest = simple_rate / 100.0
    compound_interest = compound_rate / 100.0
    
    F_simple = principal * (1 + simple_interest * n)
    F_compound = principal * (1 + compound_interest)**n

    I_simple = principal * simple_interest * np.ones(periods + 1)
    I_simple[0] = 0
    
    # Calculate Compound Interest Breakdown
    I_compound_principal = principal * compound_interest * np.ones(periods + 1)
    I_compound_principal[0] = 0
    I_compound_on_interest = np.zeros(periods + 1)
    
    for k in range(1, periods + 1):
        I_compound_on_interest[k] = (F_compound[k-1] - principal) * compound_interest

    # Build the Interactive Plot
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Future Value', 'Interest Earned Per Period')
    )
    
    # --- ROW 1: Cumulative Lines ---
    # Add Simple Interest Line
    fig.add_trace(go.Scatter(
        x=n, y=F_simple,
        mode='lines+markers',
        name=f'Total: Simple ({simple_rate}%)',
        line=dict(color='blue', dash='dash'),
        hovertemplate='Year %{x}<br>Amount: $%{y:,.2f}<extra></extra>'
    ), row=1, col=1)

    # Add Compound Interest Line
    fig.add_trace(go.Scatter(
        x=n, y=F_compound,
        mode='lines+markers',
        name=f'Total: Compound ({compound_rate}%)',
        line=dict(color='red'),
        hovertemplate='Year %{x}<br>Amount: $%{y:,.2f}<extra></extra>'
    ), row=1, col=1)

    # --- ROW 2: Period Interest Bars ---
    # Add Simple Interest Bars
    fig.add_trace(go.Bar(
        x=n, y=I_simple,
        name='Period: Simple',
        marker_color='blue',
        opacity=0.6,
        offsetgroup=0,
        hovertemplate='Year %{x} Interest: $%{y:,.2f}<extra></extra>'
    ), row=2, col=1)

    # Add Compound Interest Bars (On Principal)
    fig.add_trace(go.Bar(
        x=n, y=I_compound_principal,
        name='Compound: On Principal',
        marker_color='red',
        opacity=0.6,
        offsetgroup=1,
        hovertemplate='Year %{x} On Principal: $%{y:,.2f}<extra></extra>'
    ), row=2, col=1)

    # Add Compound Interest Bars (On Accumulated Interest)
    fig.add_trace(go.Bar(
        x=n, y=I_compound_on_interest,
        name='Compound: On Interest',
        marker_color='darkred',
        opacity=0.8,
        offsetgroup=1,
        base=I_compound_principal,
        customdata=I_compound_on_interest,
        hovertemplate='Year %{x} On Interest: $%{customdata:,.2f}<extra></extra>'
    ), row=2, col=1)

    # Formatting the layout
    fig.update_layout(
        title='Simple vs. Compound Interest Analysis',
        hovermode='x unified', # Shows all values simultaneously on hover
        template='plotly_white',
        barmode='group',       # Groups the bars side-by-side
        height=700             # Increased height to accommodate both plots
    )

    # Update axis labels
    fig.update_yaxes(title_text="Total Value ($)", row=1, col=1)
    fig.update_yaxes(title_text="Interest Value ($)", row=2, col=1)
    fig.update_xaxes(title_text="Number of Periods (years)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison Summary
    final_simple = F_simple[-1]
    final_compound = F_compound[-1]
    
    st.markdown("### 🔍 Conclusion at Year " + str(periods))
    st.write(f"- **Simple Interest:** ${final_simple:,.2f}")
    st.write(f"- **Compound Interest:** ${final_compound:,.2f}")
    
    diff = abs(final_compound - final_simple)
    if final_compound > final_simple:
        st.error(f"Compound Interest yields **${diff:,.2f} more** than Simple Interest by year {periods}.")
    elif final_simple > final_compound:
        st.success(f"Simple Interest yields **${diff:,.2f} more** than Compound Interest by year {periods}.")
    else:
        st.warning("Both yield the exact same amount.")
