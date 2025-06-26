# Sentiment Analysis Processing Script

## Overview
This script (`process_sentiments.py`) processes sentiment data from social network posts. It groups data by user and symbol, maps player levels to numeric IDs, spreads sentiment values across date ranges, and outputs a cleaned, processed CSV file. It can also generate summary statistics about the processed data.

## Features
- Groups sentiment data by `OwnerID`, `Symbol`, and `date`
- Maps `PlayerLevel` strings to numeric IDs
- Spreads each sentiment across all days until the next post or a specified end date
- Adds a `daysSincePost` column for each row
- Removes duplicates, keeping only the latest sentiment per user, symbol, and date
- Outputs processed data to a specified CSV file
- Optionally saves summary statistics to a text file

## Requirements
- Python 3.x
- pandas
- numpy

Install dependencies with:
```sh
pip install pandas numpy
```

## Usage
```sh
python process_sentiments.py --input <input_csv> --output <output_csv> [--end-date YYYY-MM-DD] [--save-stats]
```
- `--input`: (Optional) Path to the input CSV file. Defaults to `sentiments.csv` in the script directory if not provided.
- `--output`: (Optional) Path to the output CSV file. Defaults to `sentiments_processed.csv` in the script directory if not provided.
- `--end-date`: (Optional) Specify the last date to spread sentiments to (format: YYYY-MM-DD). Defaults to today.
- `--save-stats`: (Optional) Save summary statistics to `sentiments_processed_stats.txt`.

## How It Works
- Reads the input CSV file (default: `sentiments.csv`)
- Groups and processes sentiment data by user, symbol, and date
- Maps player levels to numeric IDs
- Spreads sentiment values across date ranges
- Adds `daysSincePost` and removes duplicates
- Outputs processed data to the specified CSV file
- Optionally saves summary statistics

## Example
```sh
python process_sentiments.py --input my_sentiments.csv --output my_processed.csv --end-date 2025-06-15 --save-stats
```

## Output
- Processed CSV file (default: `sentiments_processed.csv`): Cleaned and spread sentiment data with additional columns.
- (Optional) `sentiments_processed_stats.txt`: Summary statistics if `--save-stats` is used.

## Logging
- Logs progress and statistics to the console
- If `--save-stats` is used, statistics are also saved to a file
