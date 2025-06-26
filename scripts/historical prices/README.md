# get_historical_prices.py

## Overview
A Python script to fetch and save historical stock price data from the NASDAQ API for a list of tickers.

## Features
- Downloads historical daily prices (open, close) for each ticker in a CSV file
- Saves each ticker's data as a CSV file in a specified output folder
- Configurable date range, line limit, and wait time between requests
- Handles errors gracefully and skips empty lines

## Requirements
- Python 3.7+
- requests

Install dependencies:
```sh
pip install requests
```

## Usage
```sh
python get_historical_prices.py <input_file> <output_folder> [--from-date YYYY-MM-DD] [--to-date YYYY-MM-DD] [--line-limit N] [--wait-ms MS]
```
- `input_file`: Path to a CSV file containing a header `Symbol` and one ticker symbol per row
- `output_folder`: Directory to save the output CSV files
- `--from-date`: (Optional) Start date (format: YYYY-MM-DD). Defaults to 2024-01-01
- `--to-date`: (Optional) End date (format: YYYY-MM-DD). Defaults to 2025-05-31
- `--line-limit`: (Optional) Maximum number of tickers to process from the input file
- `--wait-ms`: (Optional) Milliseconds to wait between requests (default: 2000)

## How It Works
- Reads the input CSV file for ticker symbols
- Fetches historical price data from the NASDAQ API for each symbol
- Saves each symbol's data as `<TICKER>_historical.csv` in the output folder

## Example
```sh
python get_historical_prices.py spx_companies.csv output_path/ --from-date 2024-01-01 --to-date 2025-05-31 --line-limit 10 --wait-ms 1000
```

## Output
- For each ticker, a CSV file named `<TICKER>_historical.csv` is created in the output folder
- Each CSV contains columns: `date`, `open`, `close`

## Notes
- The script uses the public NASDAQ API and may be subject to rate limits or changes
- If an error occurs for a ticker, it is printed and the script continues with the next ticker
