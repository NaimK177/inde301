import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Ch1: Calculator", layout="wide")

st.title("🧮 Chapter 1 Tools")
st.markdown("Interactive tools to understand the Rule of 72 and the impact of compounding.")

# --- Sidebar Inputs ---
st.sidebar.header("Select Tool")
tool_choice = st.sidebar.radio("Tool", ["Rule of 72 Estimator", "Simple vs. Compound Interest"])

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
    
    st.sidebar.header("Input Parameters")
    principal = st.sidebar.number_input("Principal Amount ($)", value=100000.0, step=5000.0)
    simple_rate = st.sidebar.number_input("Simple Interest Rate (%)", value=8.5, step=0.1)
    compound_rate = st.sidebar.number_input("Compound Interest Rate (%)", value=6.0, step=0.1)
    periods = st.sidebar.slider("Number of Periods (Years)", min_value=1, max_value=50, value=20)
    
    # Calculate arrays
    years = list(range(periods + 1))
    simple_values = [principal * (1 + (simple_rate / 100.0) * n) for n in years]
    compound_values = [principal * (1 + (compound_rate / 100.0))**n for n in years]
    
    # Plotly Figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years, y=simple_values,
        mode='lines+markers',
        name=f'Simple Interest ({simple_rate}%)',
        line=dict(color='#3B82F6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=years, y=compound_values,
        mode='lines+markers',
        name=f'Compound Interest ({compound_rate}%)',
        line=dict(color='#EF4444', width=3)
    ))
    
    fig.update_layout(
        title="Future Value Over Time",
        xaxis_title="Years",
        yaxis_title="Total Value ($)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    st.plotly_chart(fig, width='stretch')
    
    # Comparison Summary
    final_simple = simple_values[-1]
    final_compound = compound_values[-1]
    
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
