import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

cur_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(cur_dir)
plt.style.use('ggplot')
np.random.seed(123)

"""
Parameters of the simulation
"""
df = pd.read_csv('appl.csv', delimiter= ',')
s0 = 10025
T = df['<TIME>'].max()
sigma = 2
dt = 1
q0 = 0
gamma = 0.1
k = 1.5
A = 140
sim_length = 1000



if __name__ == '__main__':
    df = pd.read_csv('appl.csv', delimiter= ',')
    """
    Variables holding inventory and P&l
    """
    inventory_s1 = [q0] * len(df['<CLOSE>'])
    pnl_s1 = [0] * len(df['<CLOSE>'])

    inventory_s2 = [q0] * len(df['<CLOSE>'])
    pnl_s2 = [0] * len(df['<CLOSE>'])

    """
    Variables holding the price properties
    that will be used in the price plot
    """


    price_a = [0] * (len(df['<CLOSE>']))
    price_b = [0] * (len(df['<CLOSE>']))
    midprice = [0] * (len(df['<CLOSE>']))
    test_time = df["<TIME>"]
    test_midprice = df['<CLOSE>']

    """
    Computation of spread for a symmetric strategy
    """
    sym_spread = 0
    for i in np.arange(0, T, dt):
        sym_spread += gamma * sigma**2 * (T - i) + \
                      (2/gamma) * np.log(1 + (gamma / k))

    av_sym_spread = (sym_spread / (T / dt))

    prob = A * np.exp(- k * av_sym_spread / 2) * dt

    """
    Simulation
    """
    for i in range(len(df['<TIME>'])):
        print(i)
        for step, s in enumerate(df['<CLOSE>']):


            """
            Inventory strategy
            """

            reservation_price = s - inventory_s1[i] * gamma * \
                                sigma**2 * (df['<TIME>'].max() - step * dt)
            spread = gamma * sigma**2 * (T - step * dt) + \
                     (2 / gamma) * np.log(1 + (gamma / k))
            spread /= 2
            if reservation_price >= s:
                ask_spread = spread + (reservation_price - s)
                bid_spread = spread - (reservation_price - s)
            else:
                ask_spread = spread - (s - reservation_price)
                bid_spread = spread + (s - reservation_price)

            ask_prob = A * np.exp(- k * ask_spread) * dt
            bid_prob = A * np.exp(- k * bid_spread) * dt
            ask_prob = max(0, min(ask_prob, 1))
            bid_prob = max(0, min(bid_prob, 1))
            ask_action_s1 = np.random.choice([1, 0],
                                             p=[ask_prob, 1 - ask_prob])
            bid_action_s1 = np.random.choice([1, 0],
                                             p=[bid_prob, 1 - bid_prob])

            inventory_s1[i] -= ask_action_s1
            pnl_s1[i] += ask_action_s1 * (s + ask_spread)
            inventory_s1[i] += bid_action_s1
            pnl_s1[i] -= bid_action_s1 * (s - bid_spread)

            if i == 0:
                price_a[step] = s + ask_spread
                price_b[step] = s - bid_spread
                midprice[step] = s

            """
            Symmetric strategy
            """

            ask_action_s2 = np.random.choice([1, 0], p=[prob, 1 - prob])
            bid_action_s2 = np.random.choice([1, 0], p=[prob, 1 - prob])
            inventory_s2[i] -= ask_action_s2
            pnl_s2[i] += ask_action_s2 * (s + av_sym_spread / 2)
            inventory_s2[i] += bid_action_s2
            pnl_s2[i] -= bid_action_s2 * (s - av_sym_spread / 2)

        pnl_s1[i] += inventory_s1[i] * s
        pnl_s2[i] += inventory_s2[i] * s

#    x_range = [-50, 150]
#    y_range = [0, 300]
    plt.figure(figsize=(16, 12), dpi=100)
#    bins = np.arange(x_range[0], x_range[1] + 1, 4)
    plt.hist(pnl_s1, bins=200, alpha=0.25,
             label="Inventory strategy")
    plt.hist(pnl_s2, bins=200, alpha=0.25,
             label="Symmetric strategy")
    plt.ylabel('P&l')
    plt.legend()
#    plt.axis(x_range + y_range)
    plt.title("The P&L histogram of the two strategies")
    plt.savefig('pnl1.pdf', bbox_inches='tight', dpi=100,
                format='pdf')


    plt.figure(figsize=(16, 12), dpi=100)
    plt.plot(df['<TIME>'], price_a, linewidth=1.0, linestyle="-",
             label="ASK")
    plt.plot(df['<TIME>'], price_b, linewidth=1.0, linestyle="-",
             label="BID")
    plt.plot(df['<TIME>'], midprice, linewidth=1.0, linestyle="-",
             label="MID-PRICE")
    plt.legend()
    plt.title("The mid-price and the optimal bid and ask quotes")
    plt.savefig('pricesdata.pdf', bbox_inches='tight', dpi=100,
                format='pdf')


    print("P&L - Mean of the inventory strategy: "
          "{}".format(np.array(pnl_s1).mean()))
    print("P&L - Mean of the symmetric strategy: "
          "{}".format(np.array(pnl_s2).mean()))
    print("P&L - Standard deviation of the inventory strategy: "
          "{}".format(np.sqrt(np.array(pnl_s1).var())))
    print("P&L - Standard deviation of the symmetric strategy: "
          "{}".format(np.sqrt(np.array(pnl_s2).var())))
    print("INV - Mean of the inventory strategy: "
          "{}".format(np.array(inventory_s1).mean()))
    print("INV - Mean of the symmetric strategy: "
          "{}".format(np.array(inventory_s2).mean()))
    print("INV - Standard deviation of the inventory strategy: "
          "{}".format(np.sqrt(np.array(inventory_s1).var())))
    print("INV - Standard deviation of the symmetric strategy: "
          "{}".format(np.sqrt(np.array(inventory_s2).var())))