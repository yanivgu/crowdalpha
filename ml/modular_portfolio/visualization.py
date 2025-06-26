import matplotlib.pyplot as plt
import os

def plot_portfolio_gains(dates, gains_dict, out_path):
    plt.figure(figsize=(12,6))
    for label, values in gains_dict.items():
        plt.plot(dates, values, label=label)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_daily_changes(dates, daily_changes_dict, out_path):
    plt.figure(figsize=(12,6))
    for label, changes in daily_changes_dict.items():
        plt.plot(dates, changes, label=label)
    plt.xlabel('Date')
    plt.ylabel('Daily Change')
    plt.title('Portfolio Daily Change Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_max_drawdown_bar(top_ns, eq_drawdowns, prop_drawdowns, out_path):
    import numpy as np
    x = np.arange(len(top_ns))
    width = 0.35
    plt.figure(figsize=(10,6))
    plt.bar(x - width/2, eq_drawdowns, width, label='Equal')
    plt.bar(x + width/2, prop_drawdowns, width, label='Proportional')
    plt.xticks(x, [f'Top {n}' for n in top_ns])
    plt.ylabel('Max Drawdown (fraction)')
    plt.title('Max Drawdown by Portfolio Type and Top N')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
