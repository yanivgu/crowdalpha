"""
process_sentiments.py
---------------------
Processes sentiment data: groups by OwnerID, sorts by CreateTime, maps PlayerLevel to IDs, and adds daysSincePost column.
"""
import os
import pandas as pd
import numpy as np
import sys
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# PlayerLevel mapping
PLAYER_LEVEL_MAP: Dict[str, int] = {
    'bronze': 1,
    'silver': 2,
    'gold': 3,
    'platinum': 4,
    'platinum plus': 5,
    'diamond': 6
}

def map_player_level(level: str) -> Optional[int]:
    """Map player level string to ID."""
    if not isinstance(level, str):
        return None
    return PLAYER_LEVEL_MAP.get(level.strip().lower())

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process and spread sentiments data.")
    parser.add_argument('--input', type=str, default=None, help='Input CSV file (default: sentiments.csv in script directory)')
    parser.add_argument('--output', type=str, default=None, help='Output CSV file (default: sentiments_processed.csv in script directory)')
    parser.add_argument('--end-date', type=str, default=None, help='End date for spreading (YYYY-MM-DD). Defaults to today.')
    parser.add_argument('--save-stats', action='store_true', default=False, help='Save statistics to file (default: False)')
    args = parser.parse_args()
    import time
    start_time = time.time()

    # Path definitions (now based on args)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sentiments_file = args.input if args.input else os.path.join(base_dir, 'sentiments.csv')
    output_file = args.output if args.output else os.path.join(base_dir, 'sentiments_processed.csv')

    # Determine end date
    if args.end_date:
        try:
            end_date = pd.to_datetime(args.end_date).date()
        except Exception as e:
            logging.error(f"Invalid end-date format: {args.end_date}. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        end_date = datetime.now().date()
    logging.info(f"Spreading up to date: {end_date}")

    if not os.path.exists(sentiments_file):
        logging.error(f"Sentiments file not found at {sentiments_file}")
        sys.exit(1)
    logging.info("Reading sentiments file...")
    try:
        df = pd.read_csv(sentiments_file)
    except Exception as e:
        logging.error(f"Failed to read sentiments file: {e}")
        sys.exit(1)
    logging.info("Sentiments file loaded.")

    if 'OwnerID' not in df.columns or 'CreateTime' not in df.columns or 'PlayerLevel' not in df.columns:
        logging.error("Required columns missing in sentiments.csv")
        sys.exit(1)
    logging.info("Filtering out internal PlayerLevel rows...")
    # Exclude rows with PlayerLevel 'internal'
    df = df[df['PlayerLevel'].str.strip().str.lower() != 'internal']
    logging.info("Mapping PlayerLevel to IDs...")
    # Map PlayerLevel to IDs
    df['PlayerLevel'] = df['PlayerLevel'].apply(map_player_level)
    if df['PlayerLevel'].isna().any():
        logging.warning("Some PlayerLevel values could not be mapped to IDs.")
    logging.info("Converting CreateTime to UTC datetime...")
    # Convert CreateTime to datetime (UTC)
    df['CreateTime'] = pd.to_datetime(df['CreateTime'], utc=True)
    logging.info("Converting CreateTime to America/New_York timezone...")
    # Calculate NYC time (America/New_York), adjust for DST
    df['CreateTime_NYC'] = df['CreateTime'].dt.tz_convert('America/New_York')
    logging.info("Calculating effective date based on NYC 09:30 cutoff...")
    # Determine 'date' column based on NYC 09:30 cutoff
    df['date'] = df['CreateTime_NYC'].apply(
        lambda dt: dt.date() if (dt.hour < 9 or (dt.hour == 9 and dt.minute < 30))
        else (dt + pd.Timedelta(days=1)).date()
    )
    # Ensure 'date' column is datetime64 for arithmetic
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop(columns=['CreateTime_NYC'])
    logging.info("Sorting and grouping by OwnerID, Symbol, and date...")
    # Group by OwnerID, Symbol, sort by date
    df = df.sort_values(['OwnerID', 'Symbol', 'date'])
    spread_rows = []
    logging.info("Spreading sentiments for each OwnerID/Symbol group...")
    for (owner, symbol), group in df.groupby(['OwnerID', 'Symbol']):
        group = group.sort_values('date')
        group = group.reset_index(drop=True)
        group['date'] = pd.to_datetime(group['date'])  # Ensure correct dtype in group
        for idx, row in group.iterrows():
            start_date = row['date']
            if isinstance(idx, (int, np.integer)) and idx < len(group) - 1:
                next_date = group.loc[idx + 1, 'date']
                # Convert next_date to pd.Timestamp if not already
                if not isinstance(next_date, (pd.Timestamp, np.datetime64)):
                    next_date = pd.Timestamp(str(next_date))
                last_date = next_date - pd.Timedelta(days=1)
            else:
                last_date = end_date
                if not isinstance(last_date, (pd.Timestamp, np.datetime64)):
                    last_date = pd.Timestamp(str(last_date))
            days = (last_date - start_date).days + 1
            for d in range(days):
                new_row = row.copy()
                new_row['date'] = start_date + pd.Timedelta(days=d)
                new_row['daysSincePost'] = d
                spread_rows.append(new_row)
    logging.info("Finished spreading sentiments. Creating final DataFrame...")
    if spread_rows:
        final_df = pd.DataFrame(spread_rows)
        logging.info("Removing duplicates and final sorting...")
        # Remove duplicates: for each owner, symbol, date, keep only the latest (should already be handled by above logic)
        final_df = final_df.sort_values(['OwnerID', 'Symbol', 'date', 'CreateTime'])
        final_df = final_df.drop_duplicates(subset=['OwnerID', 'Symbol', 'date'], keep='last')
        final_df = final_df.sort_values(['OwnerID', 'Symbol', 'date'])
        # Save to output
        logging.info("Saving processed sentiments to CSV...")
        final_df.to_csv(output_file, index=False)
        logging.info(f"Processed and spread sentiments saved to {output_file}")

        # Statistics collection
        num_users = final_df['OwnerID'].nunique() if 'OwnerID' in final_df.columns else None
        min_date = final_df['date'].min().date() if 'date' in final_df.columns else None
        max_date = final_df['date'].max().date() if 'date' in final_df.columns else None
        num_symbols = final_df['Symbol'].nunique() if 'Symbol' in final_df.columns else None
        num_rows = len(final_df)

        # Print statistics to log
        logging.info(f"Number of users: {num_users:,}")
        logging.info(f"Date range: {min_date} to {max_date}")
        logging.info(f"Number of symbols: {num_symbols:,}")
        logging.info(f"Number of rows in output: {num_rows:,}")
        # Process run time
        run_time = time.time() - start_time
        logging.info(f"Process run time: {run_time:.2f} seconds")
        # Save statistics to file if requested
        if args.save_stats:
            stats_file = os.path.join(base_dir, 'sentiments_processed_stats.txt')
            with open(stats_file, 'w') as f:
                f.write(f"num_users: {num_users:,}\n")
                f.write(f"min_date: {min_date}\n")
                f.write(f"max_date: {max_date}\n")
                f.write(f"num_symbols: {num_symbols:,}\n")
                f.write(f"num_rows: {num_rows:,}\n")
                f.write(f"process_run_time_seconds: {run_time:.2f}\n")
            logging.info(f"Statistics saved to {stats_file}")
    else:
        logging.error("No data to process after spreading.")
        sys.exit(1)

if __name__ == "__main__":
    main()
