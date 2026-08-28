import streamlit as st

st.set_page_config(page_title="Ch4: Main Ideas & Formulas", layout="wide")

st.title("💡 Chapter 4: Nominal and Effective Interest Rates")

st.markdown(r"""
### 1. Nominal Interest Rate

A nominal interest rate $r$ is a rate that does not consider compounding.

$$
r = \text{interest rate per period} \times \text{number of periods}
$$

**Note:** Nominal interest rate is commonly referred to as Annual Percentage Rate (APR).
""")

st.markdown(r"""
### 2. Effective Interest Rate

An effective interest rate $i$ is the actual or observed rate that applies for a period of time, considering compounding. It is also called the Annual Percentage Yield (APY).

If $r$ is the nominal rate per year and $m$ is the number of compounding periods per year, the effective rate per compounding period is:
$$
i = \frac{r}{m}
$$

The **effective annual interest rate**, $i_a$, is:
$$
i_a = \left(1 + \frac{r}{m}\right)^m - 1
$$
""")

st.markdown(r"""
### 3. Continuous Compounding

Continuous compounding occurs when the compounding frequency $m$ approaches infinity. 

Given a nominal annual rate $r$, the effective annual interest rate under continuous compounding is:
$$
i = e^r - 1
$$

The continuous compounding factors mirror the discrete factors, substituting $(1+i)^n$ with $e^{rt}$, where $t$ is the number of years.
*   **Compound Amount (F/P):** $F = P e^{rt}$
*   **Present Worth (P/F):** $P = F e^{-rt}$
""")

st.markdown(r"""
### 4. Bonds and Yield to Maturity

A bond is a long-term note representing debt financing.
*   **Face Value ($F$):** The amount paid back at maturity.
*   **Coupon Amount ($C$):** The interest paid periodically ($C/m$ per period).

**Yield to Maturity ($\lambda$):** The interest rate that equates the present worth of the bond's future cash flows to its current market price $P$.
$$
P = F\left(1+\frac{\lambda}{m}\right)^{-n} + \frac{C}{\lambda} \left( 1-\frac{1}{(1+\lambda/m)^n} \right)
$$
As the yield $\lambda$ increases, the price of the bond $P$ decreases.
""")

st.markdown(r"""
### 5. Time Varying Interest Rate

Interest rates may vary from one period to the next. Let the rates for periods $1, \dots, n$ be $i_1, \dots, i_n$.
The Future Worth $F$ of a Present amount $P$ after $n$ periods is:
$$
F = P \prod_{k=1}^{n} (1+i_k) = P(1+i_1)(1+i_2)\dots(1+i_n)
$$
""")
