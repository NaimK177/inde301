import numpy as np
import plotly.graph_objects as go

def plot_bond_price_vs_yield(F=1000, C=None, coupon_rate=None, m=2, years=10):
    """
    Plots the price of a bond against varying yield rates.
    
    Parameters:
    F           : Face value of the bond
    C           : Total annual coupon payment (optional, used if coupon_rate is None)
    coupon_rate : Annual coupon rate as a decimal (e.g. 0.10 for 10%)
    m           : Compounding periods per year
    years       : Years to maturity
    """
    if C is None and coupon_rate is None:
        C = 100 # default
    elif coupon_rate is not None:
        C = F * coupon_rate
        
    # Total number of periods
    n = years * m
    
    # Generate an array of yield rates (lambda) from 1% to 20%
    yields = np.linspace(0.01, 0.20, 100)
    
    # Calculate bond price for each yield using the provided formula
    # P = F*(1 + lambda/m)^(-n) + (C/lambda) * (1 - (1 + lambda/m)^(-n))
    discount_factor = (1 + yields / m)**(-n)
    present_value_face = F * discount_factor
    present_value_coupons = (C / yields) * (1 - discount_factor)
    
    prices = present_value_face + present_value_coupons
    
    # Create the Plotly figure
    fig = go.Figure()
    
    # Add the bond price curve
    fig.add_trace(go.Scatter(
        x=yields * 100, 
        y=prices,
        mode='lines',
        name='Bond Price Curve',
        line=dict(color='#ef4444', width=2)
    ))
    
    # Add the Par Value line
    fig.add_trace(go.Scatter(
        x=[1, 20],
        y=[F, F],
        mode='lines',
        name=f'Par Value (${F})',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    # Formatting the chart
    fig.update_layout(
        title=f'Bond Price vs. Yield to Maturity with m={m} over {years} years',
        xaxis_title='Yield to Maturity (λ) %',
        yaxis_title='Bond Price ($P$)',
        template='plotly_white'
    )
    
    # Return the figure
    return fig

