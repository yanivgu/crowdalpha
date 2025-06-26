import json
import argparse
import os
import csv

def get_default_output_path(input_path):
    # Get base path without extension and add .csv
    base, ext = os.path.splitext(input_path)
    if ext == '.csv':
        return input_path
    elif ext == '':
        return input_path + '.csv'
    else:
        raise ValueError("Only .csv format is supported for output files.")

def parse_tickers(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [item['symbol'] for item in data]

def write_symbols(symbols, output_path):
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Symbol'])
        for symbol in symbols:
            writer.writerow([symbol])

def main():
    parser = argparse.ArgumentParser(description='Parse ticker symbols from JSON file')
    parser.add_argument('input_path', help='Path to JSON file containing ticker data')
    parser.add_argument('--output', '-o', help='Path to output text file (optional)', default=None)
    
    args = parser.parse_args()
    
    try:
        # Determine output path
        output_path = args.output or get_default_output_path(args.input_path)
        
        # Parse and write symbols
        symbols = parse_tickers(args.input_path)
        write_symbols(symbols, output_path)
        print(f"Symbols written to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()