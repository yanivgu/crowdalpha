# Ticker Parser Script

## Overview
This script extracts ticker symbols from a JSON file and writes them to a CSV file with a header 'Symbol', one symbol per row.

## Features
- Parses a JSON file containing ticker data
- Outputs a CSV file with one symbol per row
- Allows custom output file naming
- Handles errors for missing or malformed input

## Requirements
- Python 3.x
- No external dependencies

## Usage
```sh
python ticker_parser.py <input_path> [--output OUTPUT]
```
- `<input_path>`: Path to the input JSON file containing ticker data (list of objects with a `symbol` key)
- `--output` or `-o`: (Optional) Path to the output CSV file. Defaults to the input filename with `.csv` extension

## How It Works
- Reads the input JSON file
- Extracts the `symbol` field from each object
- Writes the symbols to a CSV file with a header

## Example
Suppose you have a file `spx_companies.json`:
```json
[
  {"symbol": "AAPL", "name": "Apple Inc."},
  {"symbol": "MSFT", "name": "Microsoft Corporation"}
]
```
Run:
```sh
python ticker_parser.py spx_companies.json
```
This will create `spx_companies.csv` with:
```
Symbol
AAPL
MSFT
```
Or specify a custom output file:
```sh
python ticker_parser.py spx_companies.json --output my_tickers.csv
```

## Error Handling
- Prints an error message if the input file is missing, not valid JSON, or does not contain the expected structure
