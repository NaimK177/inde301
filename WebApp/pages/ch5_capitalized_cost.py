import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Ch5: Capitalized Cost & Payback", layout="wide")

st.title("♾️ Capitalized Cost & Payback Analysis")

st.markdown("""
This page provides interactive tools for **Capitalized Cost (CC)** analysis of infinite-life projects/endowments and **Payback Period** evaluation (including the Payback Trap visualizer).
""")

st.markdown("---")

tab1, tab2 = st.tabs(["♾️ Capitalized Cost Calculator", "⏱️ Payback Period & Trap Visualizer"])

# Helper financial functions
def pw_factor(i, n):
    return (1.0 + i) ** (-n)

def af_factor(i, n):
    if i == 0:
        return 1.0 / float(n)
    return i / ((1.0 + i)**n - 1.0)

def pa_factor(i, n):
    if i == 0:
        return float(n)
    return ((1.0 + i)**n - 1.0) / (i * (1.0 + i)**n)

# TAB 1: CAPITALIZED COST
with tab1:
    st.header("Capitalized Cost (CC) Analysis")
    st.markdown("""
    Capitalized Cost represents the Present Worth of cash flows with an **infinite useful life** ($n \\to \\infty$).
    """)
    
    cc_preset = st.radio(
        "Select CC Scenario:",
        ["AUB 'Woohoo' Software System (Course Note Example)", "Custom Infinite Project Builder"],
        horizontal=True
    )
    
    if cc_preset == "AUB 'Woohoo' Software System (Course Note Example)":
        st.subheader("🏫 American University of Beirut (AUB) - Woohoo Software System")
        st.markdown("""
        **Project Parameters:**
        - **Interest Rate ($i$):** 5.00% per year
        - **Initial Installation Cost ($t=0$):** -$150,000
        - **One-time Hardware Upgrade ($t=10$):** -$50,000
        - **Annual Maintenance:** -$5,000/yr (Years 1..4), -$8,000/yr (Years 5..$\\infty$)
        - **Major Software Upgrades:** -$15,000 every 13 years ($n_R = 13$)
        """)
        
        i_rate = 0.05
        
        # Step 1: Non-recurring
        cc_nonrec = -150000.0 - 50000.0 * pw_factor(i_rate, 10)
        
        # Step 2: Maintenance
        cc_maint_base = -5000.0 / i_rate
        cc_maint_extra = (-3000.0 / i_rate) * pw_factor(i_rate, 4)
        cc_maint_total = cc_maint_base + cc_maint_extra
        
        # Step 3: Upgrades
        a_upgrade = -15000.0 * af_factor(i_rate, 13)
        cc_upgrade = a_upgrade / i_rate
        
        cc_total = cc_nonrec + cc_maint_total + cc_upgrade
        
        st.markdown("### 🧮 Step-by-Step Capitalized Cost Breakdown")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Non-Recurring CC", f"${cc_nonrec:,.2f}")
        col2.metric("Maintenance CC", f"${cc_maint_total:,.2f}")
        col3.metric("Upgrade Cycle CC", f"${cc_upgrade:,.2f}")
        col4.metric("Total Capitalized Cost", f"${cc_total:,.2f}")
        
        st.markdown("""
        #### Detailed Calculations:
        1. **Non-Recurring Cash Flows ($t=0, t=10$):**
           $$CC_{\\text{non-rec}} = -150,000 - 50,000(P/F, 5\\%, 10) = -150,000 - 50,000(0.61391) = -\\$180,695.66$$
        2. **Maintenance Contract (Base -\\$5k + Extra -\\$3k starting Year 5):**
           $$CC_{\\text{base}} = \\frac{-5,000}{0.05} = -\\$100,000.00$$
           $$CC_{\\text{extra at } t=0} = \\left(\\frac{-3,000}{0.05}\\right)(P/F, 5\\%, 4) = -60,000(0.82270) = -\\$49,362.15$$
           $$CC_{\\text{maint}} = -100,000.00 - 49,362.15 = -\\$149,362.15$$
        3. **Recurring Major Upgrades (-\\$15k every 13 years):**
           $$A_R = -15,000(A/F, 5\\%, 13) = -15,000(0.05646) = -\\$846.84$$
           $$CC_{\\text{upgrade}} = \\frac{A_R}{0.05} = \\frac{-846.84}{0.05} = -\\$16,936.73$$
        4. **Total Capitalized Cost:**
           $$CC_{\\text{total}} = -180,695.66 - 149,362.15 - 16,936.73 = \\mathbf{-\\$346,994.54}$$
        """)
        
    else:
        st.subheader("🛠️ Custom Infinite Project Builder")
        
        i_custom_pct = st.number_input("Interest Rate i (% per year):", min_value=0.1, max_value=50.0, value=5.0, step=0.5)
        i_custom = i_custom_pct / 100.0
        
        c1, c2 = st.columns(2)
        with c1:
            p_initial = st.number_input("Initial Investment P at t=0 ($):", value=100000.0, step=10000.0)
            a_perpetual = st.number_input("Annual Perpetual Cash Flow A ($):", value=8000.0, step=1000.0, help="Positive for net income/savings, negative for annual operating costs")
        with c2:
            r_cycle = st.number_input("Recurring Overhaul/Upgrade Amount R ($):", value=20000.0, step=2000.0)
            n_cycle = st.number_input("Overhaul Cycle Interval n_R (Years):", min_value=1, max_value=100, value=10, step=1)
            
        # Calculation
        cc_init = -p_initial
        cc_ann = a_perpetual / i_custom
        a_r = -r_cycle * af_factor(i_custom, n_cycle)
        cc_r = a_r / i_custom
        
        cc_custom_total = cc_init + cc_ann + cc_r
        
        st.markdown("### 📊 Capitalized Cost Summary")
        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Initial Capital CC", f"${cc_init:,.2f}")
        mc2.metric("Perpetual Annual CC", f"${cc_ann:,.2f}")
        mc3.metric("Recurring Overhaul CC", f"${cc_r:,.2f}")
        mc4.metric("Net Capitalized Cost", f"${cc_custom_total:,.2f}")

# TAB 2: PAYBACK PERIOD & PAYBACK TRAP
with tab2:
    st.header("Payback Period Analysis & The Payback Trap")
    st.markdown("""
    The payback period $n_P$ is the time required to recover the initial investment $P$ plus interest $i$:
    $$0 = -P + \\sum_{t=1}^{n_P} NCF_t (1+i)^{-t}$$
    """)
    
    st.subheader("🚨 Demonstration: The Payback Trap (Machine X vs. Machine Y)")
    st.markdown("""
    Consider two mutually exclusive machines evaluated using a **0% Payback Method** for a 5-year project:
    - **Machine X:** Costs $10,000. Generates $2,500/year for 5 years. Salvage value = $0.
    - **Machine Y:** Costs $10,000. Generates $2,000/year for 5 years. Salvage value = **$8,000** at Year 5.
    """)
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.info("""
        **Machine X Payback:**  
        $$n_{P,X} = \\frac{10,000}{2,500} = \\mathbf{4.00 \\text{ Years}}$$  
        *Payback Decision:* Preferred because it recovers investment 1 year faster.
        """)
    with col_y:
        st.info("""
        **Machine Y Payback:**  
        $$n_{P,Y} = \\frac{10,000}{2,000} = \\mathbf{5.00 \\text{ Years}}$$  
        *Payback Decision:* Rejected compared to X.
        """)
        
    st.error("""
    ❌ **Why Payback Misleads the Decision Maker:**  
    Payback completely ignores the **$8,000 salvage value** of Machine Y in Year 5!  
    - Total Cash Generated by X: **$12,500** (Net Profit = $2,500)  
    - Total Cash Generated by Y: **$18,000** (Net Profit = $8,000)  
    Machine Y generates **3.2x more net profit**, but Payback analysis incorrectly prefers Machine X.
    """)
    
    # Visual comparison chart
    years_pb = list(range(6))
    cum_x = [-10000, -7500, -5000, -2500, 0, 2500]
    cum_y = [-10000, -8000, -6000, -4000, -2000, 8000]
    
    pb_fig = go.Figure()
    pb_fig.add_trace(go.Scatter(x=years_pb, y=cum_x, mode="lines+markers", name="Machine X Cumulative Cash Flow ($)"))
    pb_fig.add_trace(go.Scatter(x=years_pb, y=cum_y, mode="lines+markers", name="Machine Y Cumulative Cash Flow ($)"))
    pb_fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even (Payback)")
    
    pb_fig.update_layout(
        title="Cumulative Cash Flow Trajectory & Payback Points",
        xaxis_title="Year",
        yaxis_title="Cumulative Net Cash Flow ($)",
        template="plotly_white"
    )
    st.plotly_chart(pb_fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🧮 Interactive Payback Period Calculator")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    p_calc = col_in1.number_input("Initial Cost P ($):", value=10000.0, step=1000.0)
    ncf_calc = col_in2.number_input("Uniform Annual Net Cash Flow ($):", value=2500.0, step=500.0)
    i_calc_pct = col_in3.number_input("Return Rate i (%):", value=10.0, step=1.0)
    i_calc = i_calc_pct / 100.0
    
    # 0% Payback
    if ncf_calc > 0:
        np_0 = p_calc / ncf_calc
        st.markdown(f"**0% Undiscounted Payback Period ($i=0\\%$):** **{np_0:.2f} Years**")
    
    # Discounted Payback
    if i_calc > 0 and ncf_calc > 0:
        cum = -p_calc
        t = 0
        while cum < 0 and t < 50:
            t += 1
            cum += ncf_calc * pw_factor(i_calc, t)
            
        if cum >= 0:
            st.markdown(f"**Discounted Payback Period ($i={i_calc_pct:.1f}\\%$):** **{t} Years**")
        else:
            st.markdown(f"**Discounted Payback Period ($i={i_calc_pct:.1f}\\%$):** Investment is **never recovered** within 50 years at this rate.")
