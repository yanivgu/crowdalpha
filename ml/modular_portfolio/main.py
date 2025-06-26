import os
import sys
import numpy as np
from data_loader import load_and_merge_data
from feature_engineering import add_score_column, aggregate_scores, filter_date_range
from portfolio_simulation import simulate_portfolio, calculate_daily_change, calculate_max_drawdown
from visualization import plot_portfolio_gains, plot_daily_changes, plot_max_drawdown_bar
import pandas as pd
from unsupervised_weight_search_v2 import find_best_vector

BASE_DIR = os.path.dirname(__file__)
REQUIRED_HEADERS = [
    'OwnerID', 'CreateTime', 'PlayerLevel', 'TwoYearGain', 'MonthsActive',
    'Symbol', 'SentimentScore', 'date', 'daysSincePost'
]

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Portfolio baseline simulation')
    parser.add_argument('sentiments_processed', type=str, help='Path to processed sentiments CSV')
    parser.add_argument('prices_agg', type=str, help='Path to prices/gains CSV')
    args = parser.parse_args()
    report_lines = []
    def log(msg):
        print(msg)
        report_lines.append(str(msg))
    processed_sentiments_file_path = args.sentiments_processed
    prices_csv_file_path = args.prices_agg
    merged_df = load_and_merge_data(processed_sentiments_file_path, prices_csv_file_path, REQUIRED_HEADERS)
    log(f"Loaded {len(merged_df)} rows after merging.")
    # Baseline: all weights = 1
    merged_df = add_score_column(merged_df, 1, 1, 1, 1)
    agg_df = aggregate_scores(merged_df)
    agg_df = filter_date_range(agg_df, pd.to_datetime('2024-06-01'), pd.to_datetime('2025-05-31'))
    log(f"agg_df rows after date filter: {len(agg_df)}")
    temp_df = agg_df[['date', 'Symbol', 'score', 'daily_gain']].copy()
    dates, values = simulate_portfolio(temp_df, top_n=10, allocation='equal')
    if len(values) > 0:
        total_gain = (values[-1] - 1.0) * 100
        log(f"Baseline Weights: [1, 1, 1, 1], Total Gain: {total_gain:.2f}%")
    else:
        log("No valid portfolio values computed.")

    # Run unsupervised optimization and save results
    best_weights, best_gain = find_best_vector(merged_df)
    with open(os.path.join(BASE_DIR, 'unsupervised_best_weights.txt'), 'w') as f:
        f.write(f'Best weights: {best_weights}\nActual total gain: {best_gain}\n')

if __name__ == "__main__":
    main()
