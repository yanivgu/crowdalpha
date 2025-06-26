# This script generates sample files for each CSV in the data folder (and one from data/prices), outputting to data/samples.
# Usage: python generate_csv_samples.py

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
SAMPLES_DIR = os.path.join(DATA_DIR, 'samples')
PRICES_DIR = os.path.join(DATA_DIR, 'prices')
SAMPLE_ROWS = 10

os.makedirs(SAMPLES_DIR, exist_ok=True)

def sample_csv(input_path, output_path, n_rows=SAMPLE_ROWS):
    try:
        df = pd.read_csv(input_path)
        df.head(n_rows).to_csv(output_path, index=False)
        print(f"Sampled {input_path} -> {output_path}")
    except Exception as e:
        print(f"Failed to sample {input_path}: {e}")

def main():
    # Sample all CSVs in data (except prices)
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.csv'):
            in_path = os.path.join(DATA_DIR, fname)
            out_path = os.path.join(SAMPLES_DIR, f'sample_{fname}')
            sample_csv(in_path, out_path)
    # Sample one CSV from prices
    if os.path.isdir(PRICES_DIR):
        for fname in os.listdir(PRICES_DIR):
            if fname.endswith('.csv'):
                in_path = os.path.join(PRICES_DIR, fname)
                out_path = os.path.join(SAMPLES_DIR, f'sample_{fname}')
                sample_csv(in_path, out_path)
                break  # Only one file

if __name__ == '__main__':
    main()
