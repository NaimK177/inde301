import streamlit as st
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go

st.set_page_config(page_title="Ch6: Annual Worth Evaluator", layout="wide")

st.title("📊 Annual Worth Evaluator & Capital Recovery")
st.markdown("""
Evaluate economic alternatives using **Annual Worth (AW)** and **Capital Recovery (CR)** analysis.
Demonstrates the single life-cycle evaluation advantage ($AW_{\\text{1-cycle}} = AW_{\\text{LCM}}$) and permanent investment perpetuities.
""")

st.markdown("---")

tab1, tab2 = st.tabs(["📊 Annual Worth & Capital Recovery Evaluator", "♾️ Permanent Investment Calculator ($n=\\infty$)"])

# Financial factor helpers
def ap_factor(i, n):
    if i == 0:
        return 1.0 / float(n)
    return (i * (1.0 + i)**n) / ((1.0 + i)**n - 1.0)

def af_factor(i, n):
    if i == 0:
        return 1.0 / float(n)
    return i / ((1.0 + i)**n - 1.0)

def pw_factor(i, n):
    return (1.0 + i)**(-n)

# TAB 1: ANNUAL WORTH EVALUATOR
with tab1:
    st.header("Annual Worth & Capital Recovery Evaluator")
    
    preset = st.selectbox(
        "📋 Select Configuration Preset:",
        [
            "Diaper Production Facility - Mutually Exclusive Alternatives",
            "Process Improvement - Independent Projects",
            "Custom Alternatives"
        ]
    )
    
    col_marr, col_pt, col_cft = st.columns(3)
    with col_marr:
        marr_pct = st.number_input("MARR (% per year):", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        marr = marr_pct / 100.0
    with col_pt:
        if "Independent" in preset:
            project_type = st.radio("Project Classification:", ["Mutually Exclusive", "Independent"], index=1)
        else:
            project_type = st.radio("Project Classification:", ["Mutually Exclusive", "Independent"], index=0)
    with col_cft:
        cash_flow_type = st.radio("Cash Flow Type:", ["Revenue Alternatives", "Cost / Service Alternatives"])
        
    if preset == "Diaper Production Facility - Mutually Exclusive Alternatives":
        default_df = pd.DataFrame([
            {"Alternative": "Alt A (New Line)", "Initial Cost P ($)": 6000000.0, "Annual Cash Flow AOC ($)": 1825000.0, "Salvage Value S ($)": 500000.0, "Useful Life n (yrs)": 6},
            {"Alternative": "Alt B (Used Line)", "Initial Cost P ($)": 2500000.0, "Annual Cash Flow AOC ($)": 730000.0, "Salvage Value S ($)": 200000.0, "Useful Life n (yrs)": 3},
            {"Alternative": "Alt C (Co-developed)", "Initial Cost P ($)": 5000000.0, "Annual Cash Flow AOC ($)": 1095000.0, "Salvage Value S ($)": 400000.0, "Useful Life n (yrs)": 4},
        ])
    elif preset == "Process Improvement - Independent Projects":
        default_df = pd.DataFrame([
            {"Alternative": "Project 1 (Inspection)", "Initial Cost P ($)": 100000.0, "Annual Cash Flow AOC ($)": 13000.0, "Salvage Value S ($)": 0.0, "Useful Life n (yrs)": 5},
            {"Alternative": "Project 2 (Guiding System)", "Initial Cost P ($)": 16000.0, "Annual Cash Flow AOC ($)": 5000.0, "Salvage Value S ($)": 0.0, "Useful Life n (yrs)": 5},
            {"Alternative": "Project 3 (Cutting Die)", "Initial Cost P ($)": 300000.0, "Annual Cash Flow AOC ($)": 40000.0, "Salvage Value S ($)": 0.0, "Useful Life n (yrs)": 5},
        ])
    else:
        default_df = pd.DataFrame([
            {"Alternative": "Option A", "Initial Cost P ($)": 10000.0, "Annual Cash Flow AOC ($)": 3500.0, "Salvage Value S ($)": 1500.0, "Useful Life n (yrs)": 4},
            {"Alternative": "Option B", "Initial Cost P ($)": 18000.0, "Annual Cash Flow AOC ($)": 5200.0, "Salvage Value S ($)": 2500.0, "Useful Life n (yrs)": 6},
        ])
        
    st.subheader("📝 Input Alternatives")
    st.markdown("Initial Cost ($P$) should be entered as a positive expenditure amount. Annual Cash Flow ($AOC$) is positive for revenues/savings and negative for operating costs.")
    
    edited_df = st.data_editor(
        default_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Initial Cost P ($)": st.column_config.NumberColumn(format="$%.2f"),
            "Annual Cash Flow AOC ($)": st.column_config.NumberColumn(format="$%.2f"),
            "Salvage Value S ($)": st.column_config.NumberColumn(format="$%.2f"),
            "Useful Life n (yrs)": st.column_config.NumberColumn(min_value=1, max_value=100, step=1)
        }
    )
    
    if not edited_df.empty and len(edited_df) >= 1:
        results = []
        lives = [int(r["Useful Life n (yrs)"]) for _, r in edited_df.iterrows()]
        lcm_horizon = math.lcm(*lives)
        
        for _, row in edited_df.iterrows():
            name = str(row["Alternative"])
            p = float(row["Initial Cost P ($)"])
            aoc = float(row["Annual Cash Flow AOC ($)"])
            s = float(row["Salvage Value S ($)"])
            n = int(row["Useful Life n (yrs)"])
            
            # Capital Recovery: CR = -P(A/P, i, n) + S(A/F, i, n)
            cr = -p * ap_factor(marr, n) + s * af_factor(marr, n)
            aw = cr + aoc
            
            # LCM PW verification
            cycles = lcm_horizon // n
            cfs_lcm = [0.0] * (lcm_horizon + 1)
            cfs_lcm[0] -= p
            for yr in range(1, lcm_horizon + 1):
                cfs_lcm[yr] += aoc
            for c in range(1, cycles + 1):
                cend = c * n
                cfs_lcm[cend] += s
                if cend < lcm_horizon:
                    cfs_lcm[cend] -= p
            pw_lcm = sum(cfs_lcm[t] * pw_factor(marr, t) for t in range(lcm_horizon + 1))
            aw_from_lcm = pw_lcm * ap_factor(marr, lcm_horizon)
            
            results.append({
                "Alternative": name,
                "Life n (yrs)": n,
                "Capital Recovery CR ($/yr)": cr,
                "Annual Operating AOC ($/yr)": aoc,
                "Annual Worth AW ($/yr)": aw,
                "LCM Horizon (yrs)": lcm_horizon,
                "LCM Present Worth ($)": pw_lcm,
                "AW from LCM ($/yr)": aw_from_lcm
            })
            
        res_df = pd.DataFrame(results)
        
        st.markdown("### 🧮 Evaluation Results Table")
        st.dataframe(
            res_df.style.format({
                "Capital Recovery CR ($/yr)": "${:,.2f}",
                "Annual Operating AOC ($/yr)": "${:,.2f}",
                "Annual Worth AW ($/yr)": "${:,.2f}",
                "LCM Present Worth ($)": "${:,.2f}",
                "AW from LCM ($/yr)": "${:,.2f}"
            }),
            use_container_width=True
        )
        
        st.info("💡 **Life-Cycle Equivalence Proof:** Notice that `Annual Worth AW ($/yr)` (calculated over a single life cycle) identically matches `AW from LCM ($/yr)` (converted from the full multi-cycle LCM Present Worth).")
        
        # Decision recommendation
        st.subheader("💡 Decision Recommendation")
        if project_type == "Mutually Exclusive":
            if cash_flow_type == "Revenue Alternatives":
                valid = res_df[res_df["Annual Worth AW ($/yr)"] >= 0]
                if valid.empty:
                    st.warning("⚠️ All alternatives yield $AW < 0$. **Recommendation: Select Do-Nothing (DN).**")
                else:
                    best = res_df.loc[res_df["Annual Worth AW ($/yr)"].idxmax()]
                    st.success(f"✅ **Recommendation: Select {best['Alternative']}** with highest positive Annual Worth of **${best['Annual Worth AW ($/yr)']:,.2f}/year**.")
            else:
                best = res_df.loc[res_df["Annual Worth AW ($/yr)"].idxmax()]
                st.success(f"✅ **Recommendation: Select {best['Alternative']}** with lowest equivalent annual cost (least negative AW) of **${best['Annual Worth AW ($/yr)']:,.2f}/year**.")
        else: # Independent
            accepted = res_df[res_df["Annual Worth AW ($/yr)"] >= 0]
            rejected = res_df[res_df["Annual Worth AW ($/yr)"] < 0]
            if not accepted.empty:
                st.success("✅ **Accepted Independent Projects (AW ≥ 0):** " + ", ".join([f"**{r['Alternative']}** (${r['Annual Worth AW ($/yr)']:,.2f}/yr)" for _, r in accepted.iterrows()]))
            if not rejected.empty:
                st.error("❌ **Rejected Independent Projects (AW < 0):** " + ", ".join([f"**{r['Alternative']}** (${r['Annual Worth AW ($/yr)']:,.2f}/yr)" for _, r in rejected.iterrows()]))

        # Visual Single-Cycle Cash Flows
        st.subheader("📈 Single Life-Cycle Cash Flow Diagrams")
        cf_cols = st.columns(len(edited_df))
        for idx, (_, row) in enumerate(edited_df.iterrows()):
            with cf_cols[idx]:
                n = int(row["Useful Life n (yrs)"])
                p = float(row["Initial Cost P ($)"])
                a = float(row["Annual Cash Flow AOC ($)"])
                s = float(row["Salvage Value S ($)"])
                
                x_vals = list(range(n + 1))
                y_vals = [-p] + [a] * (n - 1) + [a + s]
                colors = ['#22C55E' if v >= 0 else '#EF4444' for v in y_vals]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=x_vals, y=y_vals, marker_color=colors, width=0.3))
                fig.add_hline(y=0, line_width=1, line_color="black")
                fig.update_layout(
                    title=f"{row['Alternative']} ({n} yrs)",
                    xaxis_title="Year",
                    yaxis_title="Cash Flow ($)",
                    template="plotly_white",
                    height=280,
                    margin=dict(l=10, r=10, t=35, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)

# TAB 2: PERMANENT INVESTMENTS
with tab2:
    st.header("Annual Worth of Permanent Investments ($n = \\infty$)")
    st.markdown("""
    When evaluating public projects, dams, highways, or endowments with infinite useful lives ($n = \\infty$), all cash flow components are converted into perpetual annual equivalents ($AW = CC \\times i$).
    """)
    
    perm_preset = st.radio("Select Scenario:", ["Permanent Irrigation Dam (Course Note Example)", "Custom Permanent Project Builder"], horizontal=True)
    
    if perm_preset == "Permanent Irrigation Dam (Course Note Example)":
        st.subheader("💧 Permanent Hydroelectric & Irrigation Dam")
        st.markdown("""
        **Project Parameters:**
        * **MARR ($i$):** 6.00% per year
        * **Initial Construction Cost ($t=0$):** -$10,000,000
        * **Routine Annual Operation & Maintenance ($AOC$):** -$200,000/year
        * **Non-Recurrent Inspection ($t=5$):** -$150,000
        * **Recurring Major Overhaul every 12 years ($n_R = 12$):** -$500,000
        """)
        
        i_dam = 0.06
        p_dam = 10000000.0
        aoc_dam = -200000.0
        c_dam = -150000.0
        nc_dam = 5
        r_dam = -500000.0
        nr_dam = 12
        
        # Step-by-step
        a_p = -p_dam * i_dam
        a_maint = aoc_dam
        a_c = (c_dam * i_dam) / ((1.0 + i_dam)**nc_dam)
        a_r = r_dam * af_factor(i_dam, nr_dam)
        
        aw_dam = a_p + a_maint + a_c + a_r
        cc_dam = aw_dam / i_dam
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("CapEx Annual Cost ($A_P$)", f"${a_p:,.2f}/yr")
        col2.metric("Annual O&M ($AOC$)", f"${a_maint:,.2f}/yr")
        col3.metric("Inspection ($A_C$)", f"${a_c:,.2f}/yr")
        col4.metric("Overhaul Cycle ($A_R$)", f"${a_r:,.2f}/yr")
        col5.metric("Total Annual Worth", f"${aw_dam:,.2f}/yr")
        
        st.markdown("---")
        st.markdown("""
        #### 🧮 Detailed Calculations:
        1. **Initial Construction ($P = \\$10,000,000$):**
           $$A_P = -P \\cdot i = -10,000,000 \\times 0.06 = \\mathbf{-\\$600,000.00 \\text{/yr}}$$
        2. **Routine Maintenance ($AOC = \\$200,000$):**
           $$A_{\\text{maint}} = \\mathbf{-\\$200,000.00 \\text{/yr}}$$
        3. **Non-Recurrent Structural Inspection ($C = \\$150,000$ at $t=5$):**
           $$A_C = \\frac{-150,000 \\times 0.06}{(1+0.06)^5} = \\frac{-9,000}{1.33823} = \\mathbf{-\\$6,725.29 \\text{/yr}}$$
        4. **Recurring Overhaul ($R = \\$500,000$ every 12 years):**
           $$A_R = -500,000(A/F, 6\\%, 12) = -500,000(0.05928) = \\mathbf{-\\$29,638.55 \\text{/yr}}$$
        5. **Total Equivalent Annual Cost:**
           $$AW = -600,000 - 200,000 - 6,725.29 - 29,638.55 = \\mathbf{-\\$836,363.84 \\text{/yr}}$$
           *(Equivalent Capitalized Cost: $CC = AW / i = -\\$13,939,397.33$)*
        """)
        
    else:
        st.subheader("🛠️ Custom Permanent Project Builder")
        i_perm_pct = st.number_input("Discount Rate i (% per year):", min_value=0.1, max_value=50.0, value=6.0, step=0.5)
        i_perm = i_perm_pct / 100.0
        
        cp1, cp2 = st.columns(2)
        with cp1:
            p_in = st.number_input("Initial Investment P at t=0 ($):", value=5000000.0, step=500000.0)
            aoc_in = st.number_input("Uniform Annual Operating Cash Flow AOC ($/yr):", value=-100000.0, step=10000.0)
        with cp2:
            c_in = st.number_input("One-time Non-Recurring Cost C ($):", value=50000.0, step=10000.0)
            nc_in = st.number_input("Year of Non-Recurring Cost (n_C):", min_value=1, max_value=100, value=5, step=1)
            r_in = st.number_input("Recurring Major Overhaul Amount R ($):", value=200000.0, step=20000.0)
            nr_in = st.number_input("Overhaul Cycle Interval (n_R years):", min_value=1, max_value=100, value=10, step=1)
            
        a_p_c = -p_in * i_perm
        a_aoc_c = aoc_in
        a_c_c = (-c_in * i_perm) / ((1.0 + i_perm)**nc_in)
        a_r_c = -r_in * af_factor(i_perm, nr_in)
        aw_total_c = a_p_c + a_aoc_c + a_c_c + a_r_c
        
        st.markdown("### 📊 Annual Worth Summary")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("CapEx Annual Cost", f"${a_p_c:,.2f}/yr")
        m2.metric("Annual O&M", f"${a_aoc_c:,.2f}/yr")
        m3.metric("Non-Recurring Annualized", f"${a_c_c:,.2f}/yr")
        m4.metric("Overhaul Annualized", f"${a_r_c:,.2f}/yr")
        m5.metric("Net Annual Worth", f"${aw_total_c:,.2f}/yr")
