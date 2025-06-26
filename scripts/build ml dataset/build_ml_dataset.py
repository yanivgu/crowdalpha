"""
build_ml_dataset.py
-------------------
Builds a machine learning dataset by merging sentiment data with daily price gains.
For each row in sentiments_processed.csv, matches a row from prices_agg.csv by date and symbol.
Adds a 'daily_gain' column (from prices_agg), or 0 if no match is found.
"""
import os
import pandas as pd
import numpy as np
import sys
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Path definitions
base_dir = os.path.dirname(os.path.abspath(__file__))
sentiments_file = os.path.join(base_dir, 'sentiments_processed.csv')
prices_file = os.path.join(base_dir, 'prices_agg.csv')
output_file = os.path.join(base_dir, 'ml_dataset.csv')

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build ML dataset by merging sentiments and price gains.")
    parser.add_argument('--save-stats', action='store_true', default=False, help='Save statistics to file (default: False)')
    args = parser.parse_args()
    start_time = time.time()

    if not os.path.exists(sentiments_file):
        logging.error(f"Sentiments file not found at {sentiments_file}")
        sys.exit(1)
    if not os.path.exists(prices_file):
        logging.error(f"Prices file not found at {prices_file}")
        sys.exit(1)
    try:
        sentiments_df = pd.read_csv(sentiments_file)
        prices_df = pd.read_csv(prices_file)
    except Exception as e:
        logging.error(f"Failed to read input files: {e}")
        sys.exit(1)
    # Ensure date columns are datetime
    sentiments_df['date'] = pd.to_datetime(sentiments_df['date'])
    prices_df['date'] = pd.to_datetime(prices_df['date'])
    # Merge on date and symbol
    merged_df = pd.merge(
        sentiments_df,
        prices_df[['date', 'symbol', 'daily_gain']],
        how='left',
        left_on=['date', 'Symbol'],
        right_on=['date', 'symbol']
    )
    # If no match, fill daily_gain with 0
    merged_df['daily_gain'] = merged_df['daily_gain'].fillna(0)
    # Drop the extra 'symbol' column from prices_df
    merged_df = merged_df.drop(columns=['symbol'])
    # Save to output
    merged_df.to_csv(output_file, index=False)
    logging.info(f"ML dataset saved to {output_file}")

    # Statistics collection
    num_users = merged_df['OwnerID'].nunique() if 'OwnerID' in merged_df.columns else None
    min_date = merged_df['date'].min()
    max_date = merged_df['date'].max()
    num_symbols = merged_df['Symbol'].nunique() if 'Symbol' in merged_df.columns else None
    num_rows = len(merged_df)

    stats = {
        'num_users': num_users,
        'min_date': str(min_date),
        'max_date': str(max_date),
        'num_symbols': num_symbols,
        'num_rows': num_rows
    }

    # Print statistics to log with commas and date only (no time)
    logging.info(f"Number of users: {num_users:,}")
    logging.info(f"Date range: {min_date.date()} to {max_date.date()}")
    logging.info(f"Number of symbols: {num_symbols:,}")
    logging.info(f"Number of rows in output: {num_rows:,}")
    # Process run time
    run_time = time.time() - start_time
    logging.info(f"Process run time: {run_time:.2f} seconds")
    # Save statistics to file with commas and date only if requested
    if args.save_stats:
        stats_file = os.path.join(base_dir, 'ml_dataset_stats.txt')
        with open(stats_file, 'w') as f:
            f.write(f"num_users: {num_users:,}\n")
            f.write(f"min_date: {min_date.date()}\n")
            f.write(f"max_date: {max_date.date()}\n")
            f.write(f"num_symbols: {num_symbols:,}\n")
            f.write(f"num_rows: {num_rows:,}\n")
            f.write(f"process_run_time_seconds: {run_time:.2f}\n")
        logging.info(f"Statistics saved to {stats_file}")

if __name__ == "__main__":
    main()
