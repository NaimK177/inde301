import streamlit as st
import pandas as pd

st.title("Time-Varying Interest Rate Calculator")

st.markdown("""
This calculator computes the **Present Worth ($P$)** and the **Equivalent Uniform Annual Series ($A$)** 
when the interest rate varies from one period to another.
""")

st.info("Based on Chapter 4: Time Varying Interest Rate")

# Input number of years
col_n, col_0 = st.columns(2)
with col_n:
    n_years = st.number_input("Number of Years (n)", min_value=1, max_value=30, value=4, step=1)
with col_0:
    cf_0 = st.number_input("Initial Cash Flow at Year 0 ($)", value=0.0, step=5000.0, help="Initial investment (outflow as negative) or upfront receipt")

st.subheader("Cash Flows and Interest Rates")
st.write("Enter the cash flow and the specific interest rate for each year.")

# Create a form or just input fields
default_data = pd.DataFrame({
    "Year": [i for i in range(1, n_years + 1)],
    "Cash Flow ($)": [70000.0, 70000.0, 35000.0, 25000.0][:n_years] + [0.0]*max(0, n_years-4),
    "Interest Rate (%)": [7.0, 7.0, 9.0, 10.0][:n_years] + [5.0]*max(0, n_years-4)
})

edited_df = st.data_editor(
    default_data,
    hide_index=True,
    disabled=["Year"],
    column_config={
        "Cash Flow ($)": st.column_config.NumberColumn("Cash Flow ($)", min_value=None, max_value=None, step=100.0, format="$%.2f"),
        "Interest Rate (%)": st.column_config.NumberColumn("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.001, format="%.3f%%"),
    }
)

if st.button("Calculate"):
    present_worth = float(cf_0)
    cumulative_discount_factor = 1.0
    
    # To calculate the equivalent uniform series A, we need the sum of the discount factors
    sum_discount_factors = 0.0
    
    results = []
    if cf_0 != 0:
        results.append({
            "Year": 0,
            "Cash Flow": f"${cf_0:,.2f}",
            "Interest Rate": "—",
            "Denominator (Product of 1+i)": "1.000000",
            "Present Worth (Step)": f"${cf_0:,.2f}"
        })
    
    for index, row in edited_df.iterrows():
        year = int(row["Year"])
        cf = row["Cash Flow ($)"]
        rate = row["Interest Rate (%)"] / 100.0
        
        # Multiply cumulative discount by (1 + i)
        cumulative_discount_factor *= (1 + rate)
        
        # Discounted cash flow
        discounted_cf = cf / cumulative_discount_factor
        present_worth += discounted_cf
        
        sum_discount_factors += (1.0 / cumulative_discount_factor)
        
        results.append({
            "Year": year,
            "Cash Flow": f"${cf:,.2f}",
            "Interest Rate": f"{rate*100:.3f}%",
            "Denominator (Product of 1+i)": f"{cumulative_discount_factor:.6f}",
            "Present Worth (Step)": f"${discounted_cf:,.2f}"
        })
        
    equivalent_A = present_worth / sum_discount_factors
    
    st.success(f"### Total Present Worth ($P$): ${present_worth:,.2f}")
    st.info(f"### Equivalent Uniform Annual Series ($A$): ${equivalent_A:,.2f}")
    
    st.subheader("Detailed Calculation Steps")
    st.markdown("For Year 0: $P_0 = CF_0$. For each year $t \\ge 1$: $P_t = \\frac{CF_t}{\\prod_{k=1}^t (1+i_k)}$")
    
    st.table(pd.DataFrame(results))
    
    # Calculate using average rate to show the pitfall as mentioned in notes
    avg_rate = edited_df["Interest Rate (%)"].mean() / 100.0
    if avg_rate > 0:
        factor = (avg_rate * (1 + avg_rate)**n_years) / ((1 + avg_rate)**n_years - 1)
        A_avg = present_worth * factor
        st.warning(f"""
        **Common Pitfall:** As highlighted in the course notes, if you incorrectly used the average interest rate ({avg_rate*100:.3f}%) 
        across all {n_years} years to find $A$ directly from $P$, the calculated equivalent uniform series ($A$) would be **${A_avg:,.2f}**.\n
        This is a difference of **${abs(A_avg - equivalent_A):,.2f}** from the true value! You must discount cashflows year-by-year.
        """)
