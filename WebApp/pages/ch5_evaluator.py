import streamlit as st
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go

st.set_page_config(page_title="Ch5: Alternative Evaluator", layout="wide")

st.title("⚖️ Alternative Evaluator (PW, FW, LCM & Study Period)")
st.markdown("""
Compare mutually exclusive alternatives or independent projects using **Present Worth (PW)** and **Future Worth (FW)** analysis, adhering strictly to equal-service requirement rules.
""")

st.markdown("---")

# Functions for exact financial factors
def pw_factor(i, n):
    return (1.0 + i) ** (-n)

def fw_factor(i, n):
    return (1.0 + i) ** n

def pa_factor(i, n):
    if i == 0:
        return float(n)
    return ((1.0 + i)**n - 1.0) / (i * (1.0 + i)**n)

def fa_factor(i, n):
    if i == 0:
        return float(n)
    return ((1.0 + i)**n - 1.0) / i

# Presets selection
preset = st.sidebar.selectbox(
    "📋 Select Configuration Preset:",
    [
        "Diaper Production Facility - Equal Life (5 Years)",
        "Diaper Production Facility - Different Lives (6, 3, 4 Years)",
        "Custom Alternatives"
    ]
)

st.sidebar.markdown("---")
marr_pct = st.sidebar.number_input("MARR (Minimum Attractive Rate of Return %):", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
marr = marr_pct / 100.0

project_type = st.sidebar.radio("Project Classification:", ["Mutually Exclusive", "Independent"])
cash_flow_type = st.sidebar.radio("Cash Flow Type:", ["Revenue Alternatives", "Cost / Service Alternatives"])

equal_service_method = st.sidebar.selectbox(
    "Equal Service Evaluation Method:",
    [
        "Direct Comparison (Equal Lives)",
        "Lowest Common Multiple (LCM) Approach",
        "Study Period Approach"
    ]
)

study_period = 5
if equal_service_method == "Study Period Approach":
    study_period = st.sidebar.number_input("Study Horizon (Years):", min_value=1, max_value=50, value=5, step=1)

# Default data loading based on preset
if preset == "Diaper Production Facility - Equal Life (5 Years)":
    default_df = pd.DataFrame([
        {"Alternative": "Alt A (New Line)", "Initial Cost ($)": 6000000.0, "Annual Cash Flow ($)": 1825000.0, "Salvage Value ($)": 0.0, "Expected Life (yrs)": 5, "Terminal MV at Horizon ($)": 0.0},
        {"Alternative": "Alt B (Used Line)", "Initial Cost ($)": 2500000.0, "Annual Cash Flow ($)": 730000.0, "Salvage Value ($)": 0.0, "Expected Life (yrs)": 5, "Terminal MV at Horizon ($)": 0.0},
        {"Alternative": "Alt C (Co-developed)", "Initial Cost ($)": 5000000.0, "Annual Cash Flow ($)": 1095000.0, "Salvage Value ($)": 0.0, "Expected Life (yrs)": 5, "Terminal MV at Horizon ($)": 0.0},
    ])
elif preset == "Diaper Production Facility - Different Lives (6, 3, 4 Years)":
    default_df = pd.DataFrame([
        {"Alternative": "Alt A (New Line)", "Initial Cost ($)": 6000000.0, "Annual Cash Flow ($)": 1825000.0, "Salvage Value ($)": 500000.0, "Expected Life (yrs)": 6, "Terminal MV at Horizon ($)": 1000000.0},
        {"Alternative": "Alt B (Used Line)", "Initial Cost ($)": 2500000.0, "Annual Cash Flow ($)": 730000.0, "Salvage Value ($)": 200000.0, "Expected Life (yrs)": 3, "Terminal MV at Horizon ($)": 0.0},
        {"Alternative": "Alt C (Co-developed)", "Initial Cost ($)": 5000000.0, "Annual Cash Flow ($)": 1095000.0, "Salvage Value ($)": 400000.0, "Expected Life (yrs)": 4, "Terminal MV at Horizon ($)": 0.0},
    ])
else:
    default_df = pd.DataFrame([
        {"Alternative": "Alternative 1", "Initial Cost ($)": 10000.0, "Annual Cash Flow ($)": 3000.0, "Salvage Value ($)": 1000.0, "Expected Life (yrs)": 4, "Terminal MV at Horizon ($)": 1000.0},
        {"Alternative": "Alternative 2", "Initial Cost ($)": 15000.0, "Annual Cash Flow ($)": 4200.0, "Salvage Value ($)": 2000.0, "Expected Life (yrs)": 6, "Terminal MV at Horizon ($)": 2000.0},
    ])

st.subheader("📝 Alternatives Input Data")
st.markdown("Edit data below or add dynamic alternatives. Initial Cost should be entered as a **positive number** representing the initial expenditure.")

edited_df = st.data_editor(
    default_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Initial Cost ($)": st.column_config.NumberColumn(format="$%.2f"),
        "Annual Cash Flow ($)": st.column_config.NumberColumn(format="$%.2f"),
        "Salvage Value ($)": st.column_config.NumberColumn(format="$%.2f"),
        "Terminal MV at Horizon ($)": st.column_config.NumberColumn(format="$%.2f", help="Estimated market value at end of study period if Life > Study Period"),
        "Expected Life (yrs)": st.column_config.NumberColumn(min_value=1, max_value=100, step=1)
    }
)

if edited_df.empty or len(edited_df) < 1:
    st.warning("Please provide at least one alternative.")
    st.stop()

# Extract lives list
lives = [int(row["Expected Life (yrs)"]) for _, row in edited_df.iterrows()]
has_unequal_lives = len(set(lives)) > 1

# Check for equal service violation error
if has_unequal_lives and equal_service_method == "Direct Comparison (Equal Lives)":
    st.error("""
    ❌ **Equal-Service Requirement Error!**  
    The defined alternatives have unequal expected service lives: **{} years**.  
    Direct Present Worth comparison over unequal lives is invalid because it violates the **Equal-Service Requirement**.  
    👉 **Action Required:** Change the *Equal Service Evaluation Method* in the sidebar to either **"Lowest Common Multiple (LCM) Approach"** or **"Study Period Approach"**.
    """.format(lives))
    st.stop()

# Evaluation logic based on method
st.subheader("📊 Evaluation & Decision Analysis")

results = []
timeline_data = {} # alt_name -> {year: net_cf}

if equal_service_method == "Direct Comparison (Equal Lives)":
    eval_horizon = lives[0]
    st.info(f"Evaluating equal-life alternatives over horizon **N = {eval_horizon} years** at MARR = {marr_pct:.2f}%.")
    
    for _, row in edited_df.iterrows():
        name = str(row["Alternative"])
        p = float(row["Initial Cost ($)"])
        a = float(row["Annual Cash Flow ($)"])
        s = float(row["Salvage Value ($)"])
        n = int(row["Expected Life (yrs)"])
        
        # PW calculation
        pw = -p + a * pa_factor(marr, n) + s * pw_factor(marr, n)
        fw = pw * fw_factor(marr, n)
        
        results.append({
            "Alternative": name,
            "Life (yrs)": n,
            "Evaluation Horizon (yrs)": n,
            "Present Worth PW ($)": round(pw, 2),
            "Future Worth FW ($)": round(fw, 2)
        })
        
        # Build timeline
        cfs = {0: -p}
        for yr in range(1, n + 1):
            cfs[yr] = a
        cfs[n] += s
        timeline_data[name] = cfs

elif equal_service_method == "Lowest Common Multiple (LCM) Approach":
    eval_horizon = math.lcm(*lives)
    st.info(f"Evaluating alternatives over the Lowest Common Multiple (LCM) horizon **N = {eval_horizon} years** at MARR = {marr_pct:.2f}%.")
    
    for _, row in edited_df.iterrows():
        name = str(row["Alternative"])
        p = float(row["Initial Cost ($)"])
        a = float(row["Annual Cash Flow ($)"])
        s = float(row["Salvage Value ($)"])
        life = int(row["Expected Life (yrs)"])
        
        cycles = eval_horizon // life
        
        cfs = {yr: 0.0 for yr in range(eval_horizon + 1)}
        cfs[0] -= p
        
        # Annual cash flows
        for yr in range(1, eval_horizon + 1):
            cfs[yr] += a
            
        # Reinvestments and salvages at end of cycles
        for c in range(1, cycles + 1):
            cycle_end = c * life
            cfs[cycle_end] += s
            if cycle_end < eval_horizon:
                cfs[cycle_end] -= p
                
        # Calculate PW by discounting each timeline year
        pw = sum(cfs[yr] * pw_factor(marr, yr) for yr in range(eval_horizon + 1))
        fw = pw * fw_factor(marr, eval_horizon)
        
        results.append({
            "Alternative": name,
            "Life (yrs)": life,
            "LCM Cycles": cycles,
            "Evaluation Horizon (yrs)": eval_horizon,
            "Present Worth PW ($)": round(pw, 2),
            "Future Worth FW ($)": round(fw, 2)
        })
        timeline_data[name] = cfs

else: # Study Period Approach
    eval_horizon = study_period
    st.info(f"Evaluating alternatives over a fixed Study Period horizon **N = {eval_horizon} years** at MARR = {marr_pct:.2f}%.")
    
    for _, row in edited_df.iterrows():
        name = str(row["Alternative"])
        p = float(row["Initial Cost ($)"])
        a = float(row["Annual Cash Flow ($)"])
        s = float(row["Salvage Value ($)"])
        life = int(row["Expected Life (yrs)"])
        mv_terminal = float(row.get("Terminal MV at Horizon ($)", s))
        
        cfs = {yr: 0.0 for yr in range(eval_horizon + 1)}
        cfs[0] -= p
        
        if life == eval_horizon:
            for yr in range(1, eval_horizon + 1):
                cfs[yr] += a
            cfs[eval_horizon] += s
            pw = -p + a * pa_factor(marr, eval_horizon) + s * pw_factor(marr, eval_horizon)
            
        elif life > eval_horizon:
            # Truncated at study horizon, add terminal MV
            for yr in range(1, eval_horizon + 1):
                cfs[yr] += a
            cfs[eval_horizon] += mv_terminal
            pw = -p + a * pa_factor(marr, eval_horizon) + mv_terminal * pw_factor(marr, eval_horizon)
            
        else: # life < eval_horizon
            # Do not replace. Calculate net FW at end of life, compound to study period end at MARR
            fw_net_life = a * fa_factor(marr, life) + s
            fw_net_study = fw_net_life * fw_factor(marr, eval_horizon - life)
            pw = -p + fw_net_study * pw_factor(marr, eval_horizon)
            
            # For visualization
            for yr in range(1, life + 1):
                cfs[yr] += a
            cfs[life] += s
            # Compounding from life to study horizon
            for yr in range(life + 1, eval_horizon + 1):
                cfs[yr] = 0.0 # invested at MARR
                
        fw = pw * fw_factor(marr, eval_horizon)
        
        results.append({
            "Alternative": name,
            "Life (yrs)": life,
            "Evaluation Horizon (yrs)": eval_horizon,
            "Present Worth PW ($)": round(pw, 2),
            "Future Worth FW ($)": round(fw, 2)
        })
        timeline_data[name] = cfs

res_df = pd.DataFrame(results)
st.dataframe(res_df.style.format({"Present Worth PW ($)": "${:,.2f}", "Future Worth FW ($)": "${:,.2f}"}), use_container_width=True)

# Decision recommendation
st.subheader("💡 Decision Recommendation")

if project_type == "Mutually Exclusive":
    if cash_flow_type == "Revenue Alternatives":
        # Highest positive PW
        valid_alts = res_df[res_df["Present Worth PW ($)"] >= 0]
        if valid_alts.empty:
            st.warning("⚠️ None of the mutually exclusive revenue alternatives yield a positive PW ($PW < 0$). **Recommendation: Select the Do-Nothing (DN) alternative.**")
        else:
            best_idx = res_df["Present Worth PW ($)"].idxmax()
            best_alt = res_df.loc[best_idx]
            st.success(f"✅ **Recommendation: Select {best_alt['Alternative']}** as it yields the **highest positive Present Worth** of **${best_alt['Present Worth PW ($)']:,.2f}** over the {eval_horizon}-year horizon.")
    else: # Cost Alternatives
        best_idx = res_df["Present Worth PW ($)"].idxmax() # numerically highest (least negative)
        best_alt = res_df.loc[best_idx]
        st.success(f"✅ **Recommendation: Select {best_alt['Alternative']}** as it yields the **least negative (lowest magnitude) Present Worth** of **${best_alt['Present Worth PW ($)']:,.2f}**.")
else: # Independent Projects
    accepted = res_df[res_df["Present Worth PW ($)"] >= 0]
    rejected = res_df[res_df["Present Worth PW ($)"] < 0]
    
    if not accepted.empty:
        st.success("✅ **Accepted Independent Projects (PW ≥ 0):** " + ", ".join([f"**{r['Alternative']}** (${r['Present Worth PW ($)']:,.2f})" for _, r in accepted.iterrows()]))
    if not rejected.empty:
        st.error("❌ **Rejected Independent Projects (PW < 0):** " + ", ".join([f"**{r['Alternative']}** (${r['Present Worth PW ($)']:,.2f})" for _, r in rejected.iterrows()]))

# Visual Cash Flow Timelines
st.subheader("📈 Cash Flow Timelines")

fig = go.Figure()
years = list(range(eval_horizon + 1))

for alt_name, cfs in timeline_data.items():
    cf_values = [cfs.get(yr, 0.0) for yr in years]
    fig.add_trace(go.Bar(
        x=years,
        y=cf_values,
        name=alt_name
    ))

fig.update_layout(
    title=f"Net Cash Flows over Evaluation Horizon ({eval_horizon} Years)",
    xaxis_title="Time $k$ (Years)",
    yaxis_title="Net Cash Flow ($)",
    barmode="group",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# MARR Sensitivity Curve
st.subheader("📉 Sensitivity Analysis: Present Worth vs. Interest Rate (i%)")

rates = np.linspace(0.0, 0.30, 61) # 0% to 30%
sens_fig = go.Figure()

for _, row in edited_df.iterrows():
    name = str(row["Alternative"])
    p = float(row["Initial Cost ($)"])
    a = float(row["Annual Cash Flow ($)"])
    s = float(row["Salvage Value ($)"])
    life = int(row["Expected Life (yrs)"])
    
    pw_curve = []
    mv_terminal = float(row.get("Terminal MV at Horizon ($)", s))
    for r in rates:
        if equal_service_method == "Lowest Common Multiple (LCM) Approach":
            cycles = eval_horizon // life
            val = -p
            for yr in range(1, eval_horizon + 1):
                val += a * pw_factor(r, yr)
            for c in range(1, cycles + 1):
                cend = c * life
                val += s * pw_factor(r, cend)
                if cend < eval_horizon:
                    val -= p * pw_factor(r, cend)
            pw_curve.append(val)
        elif equal_service_method == "Study Period Approach":
            if life == eval_horizon:
                val = -p + a * pa_factor(r, eval_horizon) + s * pw_factor(r, eval_horizon)
            elif life > eval_horizon:
                val = -p + a * pa_factor(r, eval_horizon) + mv_terminal * pw_factor(r, eval_horizon)
            else:
                fw_net_life = a * fa_factor(r, life) + s
                fw_net_study = fw_net_life * fw_factor(r, eval_horizon - life)
                val = -p + fw_net_study * pw_factor(r, eval_horizon)
            pw_curve.append(val)
        else:
            val = -p + a * pa_factor(r, life) + s * pw_factor(r, life)
            pw_curve.append(val)
            
    sens_fig.add_trace(go.Scatter(
        x=rates * 100,
        y=pw_curve,
        mode="lines+markers",
        name=name
    ))

sens_fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="PW = 0")
sens_fig.update_layout(
    title="Present Worth Sensitivity Curve across Interest Rates",
    xaxis_title="Interest Rate i (%)",
    yaxis_title="Present Worth ($)",
    template="plotly_white"
)
st.plotly_chart(sens_fig, use_container_width=True)
