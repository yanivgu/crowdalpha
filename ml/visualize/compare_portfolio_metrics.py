import sys
import os

# Add modular_portfolio to sys.path for imports
MODULAR_PORTFOLIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modular_portfolio'))
sys.path.insert(0, MODULAR_PORTFOLIO_DIR)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_and_merge_data
from feature_engineering import add_score_column, aggregate_scores, filter_date_range
from portfolio_simulation import simulate_portfolio, calculate_daily_change, calculate_max_drawdown, calculate_drawdown_series

# Paths (adjust if needed)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SENTIMENTS_PATH = os.path.join(BASE_DIR, 'data', 'sentiments_processed.csv')
PRICES_PATH = os.path.join(BASE_DIR, 'data', 'prices_agg.csv')
SPX_PATH = os.path.join(BASE_DIR, 'data', 'spx_prices.csv')
REQUIRED_HEADERS = [
    'OwnerID', 'CreateTime', 'PlayerLevel', 'TwoYearGain', 'MonthsActive',
    'Symbol', 'SentimentScore', 'date', 'daysSincePost'
]

# Weight vectors to compare
VECTORS = [
    np.array([0.70185104, 0.80219342, 0.68594314, 0.13002897]),
    np.array([1, 1, 1, 1])
]
VECTOR_LABELS = [
    'Optimized [0.70, 0.80, 0.69, 0.13]',
    'Baseline [1, 1, 1, 1]'
]

# Date range (adjust as needed)
START_DATE = pd.to_datetime('2024-06-01')
END_DATE = pd.to_datetime('2025-05-31')

def main():
    merged_df = load_and_merge_data(SENTIMENTS_PATH, PRICES_PATH, REQUIRED_HEADERS)
    results = []
    for vec, label in zip(VECTORS, VECTOR_LABELS):
        df = add_score_column(merged_df.copy(), *vec)
        agg_df = aggregate_scores(df)
        agg_df = filter_date_range(agg_df, START_DATE, END_DATE)
        temp_df = agg_df[['date', 'Symbol', 'score', 'daily_gain']].copy()
        dates, values = simulate_portfolio(temp_df, top_n=10, allocation='equal')
        daily_gains = calculate_daily_change(values)
        # Calculate drawdown series over time
        drawdown_series = 1 - (np.array(values) / np.maximum.accumulate(values))
        max_drawdown = np.max(drawdown_series)
        results.append({
            'label': label,
            'dates': dates,
            'values': values,
            'daily_gains': daily_gains,
            'drawdown_series': drawdown_series,
            'max_drawdown': max_drawdown
        })

    # Add SPX index
    spx_df = pd.read_csv(SPX_PATH)
    spx_df['Date'] = pd.to_datetime(spx_df['Date'])
    spx_df = spx_df[(spx_df['Date'] >= START_DATE) & (spx_df['Date'] <= END_DATE)]
    spx_df = spx_df.sort_values('Date')
    spx_close = spx_df['Close'].to_numpy()
    spx_dates = spx_df['Date'].to_list()
    spx_values = spx_close / spx_close[0]  # Normalize to 1.0 at start
    spx_daily_gains = np.diff(spx_values, prepend=spx_values[0])
    spx_drawdown_series = 1 - (spx_values / np.maximum.accumulate(spx_values))
    spx_max_drawdown = np.max(spx_drawdown_series)
    results.append({
        'label': 'SPX Index',
        'dates': spx_dates,
        'values': spx_values,
        'daily_gains': spx_daily_gains,
        'drawdown_series': spx_drawdown_series,
        'max_drawdown': spx_max_drawdown
    })

    # Plot gain over time (as percentage, starting from zero)
    plt.figure(figsize=(12, 6))
    for res in results:
        pct_gain = (np.array(res['values']) - 1.0) * 100
        plt.plot(res['dates'], pct_gain, label=res['label'])
    plt.title('Portfolio Gain Over Time (%)')
    plt.xlabel('Date')
    plt.ylabel('Gain (%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('portfolio_value_comparison.png')
    print('Saved: portfolio_value_comparison.png')
    plt.close()

    # Plot daily gain over time (as percentage, starting from zero)
    plt.figure(figsize=(12, 6))
    for res in results:
        pct_daily_gain = (np.array(res['daily_gains'][1:])) * 100
        plt.plot(res['dates'][1:], pct_daily_gain, label=res['label'])
    plt.title('Daily Gain Over Time (%)')
    plt.xlabel('Date')
    plt.ylabel('Daily Gain (%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('daily_gain_comparison.png')
    print('Saved: daily_gain_comparison.png')
    plt.close()

    # Plot drawdown over time (as percentage)
    plt.figure(figsize=(12, 6))
    for res in results:
        plt.plot(res['dates'], res['drawdown_series'] * 100, label=res['label'])
    plt.title('Drawdown Over Time (%)')
    plt.xlabel('Date')
    plt.ylabel('Drawdown (%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('drawdown_over_time_comparison.png')
    print('Saved: drawdown_over_time_comparison.png')
    plt.close()

    # Save max drawdown values to a text file
    with open('max_drawdown_values.txt', 'w') as f:
        for res in results:
            f.write(f"{res['label']}: {res['max_drawdown']*100:.2f}%\n")
    print('Saved: max_drawdown_values.txt')

if __name__ == '__main__':
    main()
