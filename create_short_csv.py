import csv
import sys
from pathlib import Path

def create_short_csv(input_file, output_file=None, num_lines=100):
    """
    Copy the header and first num_lines rows from input_file to output_file.
    If output_file is None, create a file with _short suffix.
    """
    if output_file is None:
        path = Path(input_file)
        output_file = str(path.parent / f"{path.stem}_short{path.suffix}")
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for i, row in enumerate(reader):
            writer.writerow(row)
            if i == num_lines:
                break
    print(f"Short CSV saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_short_csv.py input.csv [output.csv] [num_lines]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    num_lines = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    create_short_csv(input_file, output_file, num_lines)
