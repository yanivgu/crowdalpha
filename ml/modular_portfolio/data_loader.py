import pandas as pd
import os

def load_and_merge_data(processed_sentiments_file_path, prices_csv_file_path, required_headers=None):
    df = pd.read_csv(processed_sentiments_file_path)
    prices_df = pd.read_csv(prices_csv_file_path)
    prices_df = prices_df.rename(columns={
        'symbol': 'Symbol',
        'date': 'date',
        'daily_gain': 'daily_gain'
    })
    if required_headers:
        missing = [h for h in required_headers if h not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    # Convert columns
    df['CreateTime'] = pd.to_datetime(df['CreateTime'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    for col in ['OwnerID', 'PlayerLevel', 'MonthsActive', 'daysSincePost']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in ['TwoYearGain', 'SentimentScore']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'date' in prices_df.columns:
        prices_df['date'] = pd.to_datetime(prices_df['date'], errors='coerce')
    if 'daily_gain' in prices_df.columns:
        prices_df['daily_gain'] = pd.to_numeric(prices_df['daily_gain'], errors='coerce')
    merged_df = pd.merge(df, prices_df, on=['date', 'Symbol'], how='left', suffixes=('', '_price'))
    return merged_df
