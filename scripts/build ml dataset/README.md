# build_ml_dataset.py

## Overview
`build_ml_dataset.py` constructs a machine learning dataset by merging sentiment analysis data with daily price gains for financial symbols. It combines data from two CSV files—`sentiments_processed.csv` and `prices_agg.csv`—to produce a single dataset suitable for ML tasks, adding a `daily_gain` column to each sentiment record.

## Features
- Merges on both `date` and `symbol`/`Symbol` columns
- Fills missing `daily_gain` values with 0
- Optionally saves statistics about the resulting dataset (number of users, date range, number of symbols, number of rows, and process run time) to `ml_dataset_stats.txt`
- Logs progress and statistics to the console

## Requirements
- Python 3.x
- pandas
- numpy

Install dependencies with:

```sh
pip install pandas numpy
```

## Usage
Run the script from the command line:

```sh
python build_ml_dataset.py [--save-stats]
```

- `--save-stats`: (Optional) If provided, saves dataset statistics to `ml_dataset_stats.txt`.

## How It Works
- Reads `sentiments_processed.csv` (processed sentiment data)
- Reads `prices_agg.csv` (aggregated daily price data)
- Merges the two on `date` and `symbol`
- Fills missing `daily_gain` values with 0
- Optionally saves statistics to `ml_dataset_stats.txt`

## Example
```
python build_ml_dataset.py --save-stats
```

## Output
- `ml_dataset.csv`: The merged dataset containing sentiment and price gain data for each record.
- (Optional) `ml_dataset_stats.txt`: Statistics about the resulting dataset if `--save-stats` is used.

## Logging
- Logs are printed to the console with timestamps and log levels
- Errors (such as missing input files) will terminate the script with an error message
