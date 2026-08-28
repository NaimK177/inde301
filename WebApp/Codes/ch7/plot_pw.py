import numpy as np
import matplotlib.pyplot as plt

def calculate_pw(i, p, a, n):
    """
    Calculate Present Worth (PW) given interest rate (i), principal (p), 
    annuity (a), and periods (n).
    Since PW(0) = -P + n*A, handle i=0 separately to avoid division by zero.
    """
    if i == 0:
        return -p + n * a
    return -p + a * ((1 + i)**n - 1) / (i * (1 + i)**n)

def main():
    p = 1000
    a = 300
    n = 4
    
    # Range of interest rates from 0% to 20%
    rates = np.linspace(0, 0.60, 100)
    pws = [calculate_pw(i, p, a, n) for i in rates]
    
    # Calculate ROR (where PW = 0)
    # Using scipy.optimize to find the exact root
    from scipy.optimize import fsolve
    ror = fsolve(calculate_pw, 0.1, args=(p, a, n))[0]
    
    plt.figure(figsize=(8, 5))
    plt.plot(rates * 100, pws, label='PW vs. Interest Rate', color='b', linewidth=2)
    plt.axhline(0, color='black', linewidth=1)
    
    # Highlight ROR
    plt.plot(ror * 100, 0, 'ro')
    plt.annotate(f'i* = {ror*100:.1f}%', xy=(ror*100, 0), xytext=(ror*100+1, 20),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=12)
                 
    plt.xlabel('Interest Rate (%)')
    plt.ylabel('Present Worth ($)')
    plt.title('Present Worth vs. Interest Rate')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Save the figure
    output_path = '../../Course Notes/Notes/figures/ch7/pw_vs_i.pdf'
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    main()
