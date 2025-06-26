"""
calculate_daily_gains.py
-----------------------
Aggregates daily percentage gains for S&P 500 companies from historical price CSVs.
Outputs a combined CSV with date, symbol, and daily gain.
"""
import os
import pandas as pd
import numpy as np
import sys
import logging
from datetime import datetime
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Path definitions
base_dir = os.path.dirname(os.path.abspath(__file__))
prices_dir = os.path.join(base_dir, 'prices')
spx_companies_file = os.path.join(base_dir, 'spx_companies.txt')
output_file = os.path.join(base_dir, 'prices_agg.csv')

def read_spx_companies(filepath: str) -> List[str]:
    """Read S&P 500 company symbols from a file."""
    if not os.path.exists(filepath):
        logging.error(f"SPX companies file not found at {filepath}")
        sys.exit(1)
    companies = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('//'):
                companies.append(line)
    if not companies:
        logging.error("No companies found in the SPX file")
        sys.exit(1)
    return companies

def process_company(symbol: str, prices_dir: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Process a single company's historical price data and return a DataFrame with daily gains.
    Daily gain is calculated as the percentage difference between open and close prices for each day.
    Returns (result_df, warning_message)
    """
    file_symbol = symbol.replace('.', '_') if '.' in symbol else symbol
    file_path = os.path.join(prices_dir, f"{file_symbol}_historical.csv")
    if not os.path.exists(file_path):
        return None, f"Warning: Price data for {symbol} not found at {file_path}"
    try:
        df = pd.read_csv(file_path)
        # Remove commas from open and close columns if present
        for col in ['open', 'close']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        expected_columns = ['date', 'open', 'close']
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            return None, f"Required columns missing in {file_path}: {missing_columns}"
        df['date'] = pd.to_datetime(df['date'])
        df['open'] = pd.to_numeric(df['open'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        warning = None
        if df['open'].isna().any() or df['close'].isna().any():
            warning = f"Warning: {file_symbol} contains missing or non-numeric open/close values"
            df = df.dropna(subset=['open', 'close'])
        df = df.sort_values('date')
        # Calculate daily gain as (close - open) / open * 100
        df['daily_gain'] = (df['close'] - df['open']) / df['open'] * 100
        df['symbol'] = symbol
        result_df = df[['date', 'symbol', 'daily_gain']]
        return result_df, warning
    except pd.errors.EmptyDataError:
        return None, f"Error: Empty data file for {symbol}"
    except FileNotFoundError:
        return None, f"Error: File not found for {symbol}"
    except Exception as e:
        return None, f"Fatal error processing {symbol}: {str(e)}"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Aggregate daily percentage gains for S&P 500 companies.")
    parser.add_argument('--save-stats', action='store_true', default=False, help='Save statistics to file (default: False)')
    args = parser.parse_args()
    import time
    start_time = time.time()

    companies = read_spx_companies(spx_companies_file)
    if not os.path.exists(prices_dir):
        logging.error(f"Prices directory not found at {prices_dir}")
        sys.exit(1)
    logging.info(f"Found {len(companies)} companies in SPX list")
    results = []
    warnings = []
    for symbol in companies:
        result_df, warning = process_company(symbol, prices_dir)
        if warning:
            warnings.append(warning)
        if result_df is not None:
            results.append(result_df)
            logging.info(f"Processed {symbol}")
    if results:
        final_df = pd.concat(results, ignore_index=True)
        # Remove rows where daily_gain is not a number (NaN or inf)
        final_df = final_df[pd.to_numeric(final_df['daily_gain'], errors='coerce').notna()]
        if final_df.empty:
            logging.error("No data was processed. Results DataFrame is empty.")
            sys.exit(1)
        final_df.to_csv(output_file, index=False)
        logging.info(f"Successfully saved all daily gains to {output_file}")
        logging.info(f"Total companies processed: {final_df['symbol'].nunique()}")

        # Statistics collection
        min_date = final_df['date'].min().date() if 'date' in final_df.columns else None
        max_date = final_df['date'].max().date() if 'date' in final_df.columns else None
        num_symbols = final_df['symbol'].nunique() if 'symbol' in final_df.columns else None
        num_rows = len(final_df)

        # Print statistics to log
        logging.info(f"Date range: {min_date} to {max_date}")
        logging.info(f"Number of symbols: {num_symbols:,}")
        logging.info(f"Number of rows in output: {num_rows:,}")
        # Process run time
        run_time = time.time() - start_time
        logging.info(f"Process run time: {run_time:.2f} seconds")
        # Save statistics to file if requested
        if args.save_stats:
            stats_file = os.path.join(base_dir, 'prices_agg_stats.txt')
            with open(stats_file, 'w') as f:
                f.write(f"min_date: {min_date}\n")
                f.write(f"max_date: {max_date}\n")
                f.write(f"num_symbols: {num_symbols:,}\n")
                f.write(f"num_rows: {num_rows:,}\n")
                f.write(f"process_run_time_seconds: {run_time:.2f}\n")
            logging.info(f"Statistics saved to {stats_file}")
    else:
        logging.error("No data was processed. Results is empty.")
        sys.exit(1)
    if warnings:
        logging.warning(f"Encountered {len(warnings)} warning(s) during processing:")
        for w in warnings:
            logging.warning(w)

if __name__ == "__main__":
    main()
