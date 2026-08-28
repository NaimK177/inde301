import streamlit as st
import numpy as np

st.set_page_config(page_title="Ch4: Nominal & Effective Rates", layout="wide")

st.title("🔄 Nominal vs Effective Interest Rate Calculator")
st.markdown("Calculate the actual observed interest rate over a year (Effective Rate/APY) given a stated Nominal Rate (APR) and a compounding frequency.")

st.header("Input Parameters")
r_pct = st.number_input("Nominal Annual Rate (APR) %", min_value=0.0, value=12.0, step=0.5)
r = r_pct / 100.0

compounding_options = {
    "Annually (1)": 1,
    "Semi-Annually (2)": 2,
    "Quarterly (4)": 4,
    "Monthly (12)": 12,
    "Weekly (52)": 52,
    "Daily (365)": 365,
    "Continuously (∞)": np.inf
}

compounding_freq = st.selectbox("Compounding Frequency (m)", list(compounding_options.keys()), index=3)
m = compounding_options[compounding_freq]

st.markdown("---")
st.header("Results")

if m == np.inf:
    # Continuous Compounding
    effective_rate = np.exp(r) - 1
    st.write(f"### Effective Annual Rate: **{effective_rate * 100:.4f}%**")
    st.info(f"Formula used: $i_a = e^{r} - 1$")
else:
    # Discrete Compounding
    effective_rate = (1 + r / m)**m - 1
    st.write(f"### Effective Annual Rate: **{effective_rate * 100:.4f}%**")
    st.info(f"Formula used: $i_a = (1 + \\frac{{{r}}}{{{m}}})^{{{m}}} - 1$")

st.markdown("---")
st.subheader("Comparison across frequencies")
# Show a table of how the effective rate changes with frequency for the given nominal rate
st.write(f"For a Nominal Rate of **{r_pct}%**, here is the effective rate across different compounding periods:")

comparison_data = []
for name, freq in compounding_options.items():
    if freq == np.inf:
        rate = np.exp(r) - 1
    else:
        rate = (1 + r / freq)**freq - 1
    comparison_data.append({"Compounding": name, "Effective Rate (%)": f"{rate * 100:.4f}%"})

st.table(comparison_data)
