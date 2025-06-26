import csv

input_path = r"C:\Users\yanivgu\Downloads\gains_2025_06_01.rpt"
output_path = "gains_2025_06_01.csv"

with open(input_path, "r") as infile, open(output_path, "w", newline="") as outfile:
    reader = infile.readlines()
    writer = csv.writer(outfile)
    writer.writerow(["id", "gain"])

    # Skip header lines
    data_lines = [line.strip() for line in reader if line.strip()]
    # Find the first line after the header separator
    for i, line in enumerate(data_lines):
        if set(line) == {'-'}:
            data_lines = data_lines[i+1:]
            break

    for line in data_lines:
        parts = line.split()
        if len(parts) == 2:
            cid, gain = parts
            try:
                gain = float(gain) * 100
                writer.writerow([cid, f"{gain:.4f}"])
            except ValueError:
                continue
