import argparse
import time
from pathlib import Path
import requests
from datetime import datetime, timedelta
import csv
import json

def get_date_range(from_date: str = None, to_date: str = None):
    # Set new default dates
    DEFAULT_FROM_DATE = '2024-01-01'
    DEFAULT_TO_DATE = '2025-05-31'
    end_date = datetime.strptime(to_date, '%Y-%m-%d') if to_date else datetime.strptime(DEFAULT_TO_DATE, '%Y-%m-%d')
    start_date = (
        datetime.strptime(from_date, '%Y-%m-%d') if from_date 
        else datetime.strptime(DEFAULT_FROM_DATE, '%Y-%m-%d')
    )
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def fetch_historical_data(ticker: str, from_date: str, to_date: str):
    url = f"https://api.nasdaq.com/api/quote/{ticker}/historical"
    params = {
        "assetclass": "stocks",
        "fromdate": from_date,
        "todate": to_date,
        "limit": 10000
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return data.get('data', {}).get('tradesTable', {}).get('rows', [])

def process_tickers(input_file: str, output_folder: str, from_date: str = None, 
                   to_date: str = None, line_limit: int = None, wait_ms: int = 2000):
    output_path = Path(output_folder)
    if output_path.exists() and not output_path.is_dir():
        raise ValueError(f"Output path '{output_folder}' exists and is not a directory.")
    output_path.mkdir(parents=True, exist_ok=True)
    from_date, to_date = get_date_range(from_date, to_date)
    
    # Read tickers from CSV file with 'Symbol' header
    tickers = []
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbol = row.get('Symbol', '')
            if symbol is not None:
                symbol = str(symbol).strip()
                if symbol:
                    tickers.append(symbol)
    
    if line_limit is not None:
        tickers = tickers[:line_limit]
    
    for ticker in tickers:
        ticker = ticker.strip()
        if not ticker:
            continue
            
        print(f"Processing ticker: {ticker}")
        output_file = Path(output_folder) / f"{ticker}_historical.csv"
        
        try:
            historical_data = fetch_historical_data(ticker, from_date, to_date)
            
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['date', 'open', 'close'])
                
                for row in historical_data:
                    open_price = row.get('open', '').replace('$', '').strip()
                    close_price = row.get('close', '').replace('$', '').strip()
                    writer.writerow([row.get('date', ''), open_price, close_price])
                    
            print(f"Data saved to {output_file}")
            
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            
        time.sleep(wait_ms / 1000)

def main():
    parser = argparse.ArgumentParser(description='Process stock tickers with configurable parameters')
    parser.add_argument('input_file', help='Path to text file containing tickers')
    parser.add_argument('output_folder', help='Path to output folder')
    parser.add_argument('--from-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--line-limit', type=int, help='Number of lines to process (optional)')
    parser.add_argument('--wait-ms', type=int, default=2000, help='Wait time in milliseconds (default: 2000)')
    
    args = parser.parse_args()
    
    process_tickers(args.input_file, args.output_folder, args.from_date, 
                   args.to_date, args.line_limit, args.wait_ms)

if __name__ == '__main__':
    main()