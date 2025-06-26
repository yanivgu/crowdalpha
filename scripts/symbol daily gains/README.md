# calculate_daily_gains.py

## Overview
A Python script to aggregate daily percentage gains for S&P 500 companies from historical price CSVs.

## Features
- Reads a list of S&P 500 ticker symbols from a text file
- Loads historical price data for each symbol from CSV files
- Calculates daily percentage gain as `(close - open) / open * 100` for each trading day
- Outputs a combined CSV file with columns: `date`, `symbol`, `daily_gain`
- Optionally saves summary statistics to a text file
- Logs processing statistics and warnings for missing or malformed data

## Requirements
- Python 3.7+
- pandas
- numpy

Install dependencies:
```sh
pip install pandas numpy
```

## Usage
```sh
python calculate_daily_gains.py [--save-stats]
```
- `--save-stats`: (Optional) Save summary statistics to a text file (`prices_agg_stats.txt`).

## How It Works
- Reads `spx_companies.txt` for ticker symbols
- Loads historical price data from `prices/` for each symbol
- Calculates daily percentage gain for each trading day
- Outputs `prices_agg.csv` with columns: `date`, `symbol`, `daily_gain`
- Optionally saves summary statistics if `--save-stats` is used

## Example
Example `spx_companies.txt`:
```
AAPL
MSFT
GOOGL
... 
```
Example `AAPL_historical.csv`:
```
date,open,close
2024-01-02,181.15,182.50
2024-01-03,182.00,180.75
... 
```

## Output
- `prices_agg.csv`: Combined CSV with columns: `date`, `symbol`, `daily_gain`
- (Optional) `prices_agg_stats.txt`: Summary statistics if `--save-stats` is used

## Logging & Warnings
- Logs progress and warnings for missing files or malformed data
- Prints summary statistics including date range, number of symbols, and total rows processed
