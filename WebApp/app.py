import streamlit as st

st.set_page_config(page_title="Engineering Economy Hub", layout="wide")

# Define the hierarchical navigation structure
pages = {
    "Chapter 1: Foundations": [
        st.Page("pages/ch1_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch1_calculator.py", title="Interactive Tools", icon="🧮"),
    ],
    "Chapter 2: Time Value of Money": [
        st.Page("pages/ch2_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch2_calculator.py", title="Interactive Calculator", icon="📈"),
        st.Page("pages/ch2_amortization.py", title="Amortization Schedule", icon="📊"),
    ],
    "Chapter 4: Nominal & Effective Interest Rates / Bonds": [
        st.Page("pages/ch4_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch4_effective.py", title="Nominal & Effective Rates", icon="🔄"),
        st.Page("pages/ch4_time_varying.py", title="Time-Varying Rates", icon="📈"),
        st.Page("pages/ch4_bonds.py", title="Bonds Calculator", icon="💵"),
    ],
    "Chapter 5: Present Worth & Economic Criteria": [
        st.Page("pages/ch5_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch5_evaluator.py", title="Alternative Evaluator (PW, FW, LCM, Study Period)", icon="⚖️"),
        st.Page("pages/ch5_capitalized_cost.py", title="Capitalized Cost & Payback Analysis", icon="♾️"),
    ],
    "Chapter 6: Annual Worth Analysis": [
        st.Page("pages/ch6_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch6_evaluator.py", title="Annual Worth Evaluator & Capital Recovery", icon="📊"),
    ],
    "Chapter 7: Rate of Return": [
        st.Page("pages/ch7_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch7_ror.py", title="Rate of Return Solver", icon="📈"),
        st.Page("pages/ch7_rules.py", title="Descartes vs Norstrom", icon="📜"),
    ],
    "Chapter 8: ROR (Multiple Alternatives)": [
        st.Page("pages/ch8_theory.py", title="Main Ideas & Formulas", icon="💡"),
        st.Page("pages/ch8_steps.py", title="Step-by-Step Guide", icon="📋"),
        st.Page("pages/ch8_incremental.py", title="Incremental ROR Solver", icon="⚖️"),
    ]
}

# Initialize and run the router
pg = st.navigation(pages)
pg.run()
