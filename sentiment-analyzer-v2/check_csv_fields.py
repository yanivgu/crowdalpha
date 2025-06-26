import sys

def parse_csv_line(line):
    result = []
    if line is None:
        return result
    i = 0
    length = len(line)
    while i < length:
        if line[i] == '"':
            i += 1  # skip opening quote
            sb = []
            in_quotes = True
            while i < length and in_quotes:
                if line[i] == '"':
                    if i + 1 < length and line[i + 1] == '"':
                        sb.append('"')
                        i += 2
                    else:
                        in_quotes = False
                        i += 1
                else:
                    sb.append(line[i])
                    i += 1
            # Skip comma after quoted field
            while i < length and line[i] != ',':
                i += 1
            if i < length and line[i] == ',':
                i += 1
            result.append(''.join(sb))
        else:
            start = i
            while i < length and line[i] != ',':
                i += 1
            result.append(line[start:i])
            if i < length and line[i] == ',':
                i += 1
    return result

if len(sys.argv) < 2:
    print("Usage: python check_csv_fields.py <csvfile> [expected_fields]")
    sys.exit(1)

csvfile = sys.argv[1]
expected_fields = int(sys.argv[2]) if len(sys.argv) > 2 else 3

with open(csvfile, encoding='utf-8') as f:
    header = f.readline()
    line_num = 1
    for line in f:
        line_num += 1
        line = line.strip()
        if not line:
            continue
        fields = parse_csv_line(line)
        if len(fields) != expected_fields:
            print(f"Line {line_num}: {len(fields)} fields: {line}")
