import pandas as pd
import plotly.graph_objects as go

# ==========================================
# Core Mathematical Factors
# ==========================================

def calculate_fp(i: float, n: int, p: float = 1.0) -> float:
    """Calculate Future Worth given Present Worth (F/P)"""
    assert n >= 0, "Number of periods (n) must be non-negative."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    return p * (1 + i)**n

def calculate_pf(i: float, n: int, f: float = 1.0) -> float:
    """Calculate Present Worth given Future Worth (P/F)"""
    assert n >= 0, "Number of periods (n) must be non-negative."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    return f * (1 + i)**-n

def calculate_pa(i: float, n: int, a: float = 1.0) -> float:
    """Calculate Present Worth given Uniform Series (P/A)"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if i == 0:
        return a * n
    return a * (((1 + i)**n - 1) / (i * (1 + i)**n))

def calculate_fa(i: float, n: int, a: float = 1.0) -> float:
    """Calculate Future Worth given Uniform Series (F/A)"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if i == 0:
        return a * n
    return a * (((1 + i)**n - 1) / i)

def calculate_ap(i: float, n: int, p: float = 1.0) -> float:
    """Calculate Uniform Series given Present Worth (A/P)"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if i == 0:
        return p / n
    return p * (i * (1 + i)**n) / ((1 + i)**n - 1)

def calculate_af(i: float, n: int, f: float = 1.0) -> float:
    """Calculate Uniform Series given Future Worth (A/F)"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if i == 0:
        return f / n
    return f * i / ((1 + i)**n - 1)

def calculate_pg(i: float, n: int, g: float = 1.0) -> float:
    """Calculate Present Worth given Arithmetic Gradient (P/G)"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if i == 0:
        return g * (n * (n - 1)) / 2
    return g * (((1 + i)**n - i * n - 1) / (i**2 * (1 + i)**n))

def calculate_ag(i: float, n: int, g: float = 1.0) -> float:
    """Calculate Uniform Series given Arithmetic Gradient (A/G)"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if i == 0:
        return g * (n - 1) / 2
    return g * ((1 / i) - (n / ((1 + i)**n - 1)))

def calculate_composite_pg(i: float, n: int, a: float, g: float) -> float:
    """Calculate Total Present Worth for a Composite Arithmetic Gradient"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    return calculate_pa(i, n, a) + calculate_pg(i, n, g)

def calculate_composite_ag(i: float, n: int, a: float, g: float) -> float:
    """Calculate Total Uniform Series for a Composite Arithmetic Gradient"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    return a + calculate_ag(i, n, g)

def calculate_geometric_pg(i: float, n: int, a1: float, g: float) -> float:
    """Calculate Total Present Worth for a Geometric Gradient"""
    assert n > 0, "Number of periods (n) must be strictly positive."
    assert i > -1.0, "Interest rate (i) must be strictly greater than -1."
    if abs(i - g) < 1e-9:
        return n * a1 / (1 + i)
    if i == 0.0:
        return a1 * (((1 + g)**n - 1) / g)
    return a1 * ((((1 + g) / (1 + i))**n - 1) / (g - i))

# ==========================================
# Amortization Table Generation
# ==========================================

def generate_amortization_schedule(principal: float, i: float, n: int) -> pd.DataFrame:
    """
    Generates a full amortization schedule.
    
    Returns:
        pandas.DataFrame: A table containing the period, previous balance,
        payment, interest, principal paid, and new balance.
    """
    payment = calculate_ap(i, n, p=principal)
    
    schedule = []
    balance = principal
    
    for period in range(1, n + 1):
        interest = balance * i
        principal_paid = payment - interest
        new_balance = balance - principal_paid
        
        # Rounding to prevent floating point errors at the last period
        if abs(new_balance) < 1e-6:
            new_balance = 0.0
            
        schedule.append({
            'Period': period,
            'Previous Balance': round(balance, 2),
            'Payment (A)': round(payment, 2),
            'Interest': round(interest, 2),
            'Principal Paid': round(principal_paid, 2),
            'New Balance': round(new_balance, 2)
        })
        
        balance = new_balance
        
    return pd.DataFrame(schedule)


# ==========================================
# Interactive Visualizations (Plotly)
# ==========================================

def plot_amortization_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Plots the proportion of a payment going toward Interest vs Principal.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['Principal Paid'],
        name='Principal Paid',
        marker_color='#2563EB'  # Blue
    ))
    
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['Interest'],
        name='Interest Paid',
        marker_color='#EF4444'  # Red
    ))
    
    fig.update_layout(
        barmode='stack',
        title='Amortization Payment Breakdown',
        xaxis_title='Period',
        yaxis_title='Amount ($)',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def plot_cash_flow(periods: list, amounts: list, title: str = "Cash Flow Diagram") -> go.Figure:
    """
    Generates an interactive cash flow diagram using Plotly.
    """
    fig = go.Figure()

    # Determine colors: Green for positive (inflow), Red for negative (outflow)
    colors = ['#22C55E' if amt > 0 else '#EF4444' for amt in amounts]

    fig.add_trace(go.Bar(
        x=periods,
        y=amounts,
        marker_color=colors,
        width=0.2,
        name='Cash Flow'
    ))

    # Add a horizontal line at y=0 to represent the time axis
    fig.add_hline(y=0, line_width=2, line_color="black")

    fig.update_layout(
        title=title,
        xaxis_title='Time Period',
        yaxis_title='Amount ($)',
        template='plotly_white',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1)
    )

    return fig

# if __name__ == '__main__':
#     # Test with Bart's Car Loan Example
#     principal = 120000
#     rate = 0.005833  # 7% / 12
#     periods = 60
    
#     print("Testing calculate_ap...")
#     payment = calculate_ap(rate, periods, p=principal)
#     print(f"Monthly Payment: ${payment:,.2f}")
#     assert round(payment, 2) == 2376.14
    
#     print("\nGenerating Amortization Schedule...")
#     df = generate_amortization_schedule(principal, rate, periods)
#     print(df.head())
#     print("...")
#     print(df.tail())
    
#     print("\nAll tests passed!")
