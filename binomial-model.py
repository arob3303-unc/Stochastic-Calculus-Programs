import numpy as np
import math
import matplotlib.pyplot as plt

# Goal -> Create a multiperiod binomial pricing model to calculate an Options price from a strike price (k).
# Most likely use the European Options market. No early exercising.
# Referencing Stochastic Calculus for Finance I book from Shreeve.

def option_price(stockPrice, strikePrice, time, rate, upFactor, downFactor, optionType='call'):
    # Assume a no-arbitrage condition.
    # time will be in days (# of periods).

    K = strikePrice
    S0 = stockPrice
    u = upFactor
    d = downFactor
    r = rate
    N = time
    p = (1 + r - d) / (u - d) # discrete risk-neutral probabilities
    discount = 1 / (1 + r)

    if d > 1 + r:
        return 'invalid down parameter! ARBITRAGE DETECTED'
    if u < 1 + r:
        return 'invalid up parameter! ARBITRAGE DETECTED'
    


    # final stock price
    ST = np.array([S0 * (u ** j) * (d ** (N - j)) for j in range (N +1)])

    if optionType == 'call':
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)
    
    for i in range(N, 0, -1):
        payoff = discount * (p * payoff[1:] + (1-p) * payoff[:-1])
    
    return payoff[0]

def plot_option_price(stockPrice, strikePrice, time, rate, upFactor, downFactor, optionType='call'):
    K = strikePrice
    S0 = stockPrice
    u = upFactor
    d = downFactor
    r = rate
    N = time
    p = (1 + r - d) / (u - d)
    discount = 1 / (1 + r)
    ST = np.array([S0 * (u ** j) * (d ** (N - j)) for j in range(N + 1)])
    
    if optionType == 'call':
        payoff = np.maximum(ST - K, 0)
    else:
        payoff = np.maximum(K - ST, 0)
    
    probs = np.array([math.comb(N, j) * (p ** j) * (1 - p) ** (N - j) for j in range(N + 1)])
    expected_contributions = probs * payoff * discount ** N

    plt.figure(figsize=(10, 6))
    plt.plot(range(N + 1), ST, 'bo-', label='Final Stock Prices')
    plt.plot(range(N + 1), payoff, 'ro-', label='Option Payoff (Raw)')
    plt.bar(range(N + 1), expected_contributions, alpha=0.4, label='Discounted Weighted Contribution')

    plt.axhline(option_price(stockPrice, strikePrice, time, rate, upFactor, downFactor, optionType), 
                color='green', linestyle='--', label='Option Price Today')

    plt.xlabel('Number of Up Moves')
    plt.ylabel('Value')
    plt.title(f'{optionType.capitalize()} Option: Final Prices, Payoff, and Weighted Contributions (N={N})')
    plt.legend()
    plt.grid(True)
    plt.show()

price = option_price(100, 100, 5, 0.05, 1.1, 0.9,'call')
plot_price = plot_option_price(100, 100, 5,.05, 1.1, 0.9,'call')

print(f"Option Price: {price:.2f}") # ANSWER should be 10.71
print(plot_price)