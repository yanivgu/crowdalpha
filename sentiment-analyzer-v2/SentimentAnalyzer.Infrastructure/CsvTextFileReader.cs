using System.Collections.Generic;
using System.IO;
using System.Threading;
using System;
using System.Threading.Tasks;
using SentimentAnalyzer.Domain;

namespace SentimentAnalyzer.Infrastructure;

public class CsvTextFileReader
{
    private readonly ILogger _logger;
    public CsvTextFileReader(ILogger logger) { _logger = logger; }
    public CsvTextFileReader() { }

    private static List<string> ParseCsvLine(string line)
    {
        var result = new List<string>();
        if (line == null)
            return result;
        int i = 0;
        while (i < line.Length)
        {
            if (line[i] == '"')
            {
                // Quoted field
                i++; // skip opening quote
                var start = i;
                var sb = new System.Text.StringBuilder();
                bool inQuotes = true;
                while (i < line.Length && inQuotes)
                {
                    if (line[i] == '"')
                    {
                        if (i + 1 < line.Length && line[i + 1] == '"')
                        {
                            // Escaped quote
                            sb.Append('"');
                            i += 2;
                        }
                        else
                        {
                            // End of quoted field
                            inQuotes = false;
                            i++;
                        }
                    }
                    else
                    {
                        sb.Append(line[i]);
                        i++;
                    }
                }
                // Skip comma after quoted field
                while (i < line.Length && line[i] != ',') i++;
                if (i < line.Length && line[i] == ',') i++;
                result.Add(sb.ToString());
            }
            else
            {
                // Unquoted field
                var start = i;
                while (i < line.Length && line[i] != ',') i++;
                result.Add(line.Substring(start, i - start));
                if (i < line.Length && line[i] == ',') i++;
            }
        }
        return result;
    }

    public async IAsyncEnumerable<T> ReadLinesAsync<T>(string filePath, ICsvAdapter<T> adapter, [System.Runtime.CompilerServices.EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        if (!File.Exists(filePath))
            throw new FileNotFoundException($"CSV file not found: {filePath}");
        using var stream = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.Read, 4096, true);
        using var reader = new StreamReader(stream);
        string headerLine = null;
        IReadOnlyList<string> fileHeaders = null;
        if (!reader.EndOfStream)
        {
            headerLine = await reader.ReadLineAsync();
            if (string.IsNullOrWhiteSpace(headerLine))
            {
                // No header line, warn and assume order
                fileHeaders = adapter.Headers;
                _logger?.Warn($"No header line found in file '{filePath}'. Assuming column order matches adapter headers.");
            }
            else
            {
                var splitHeaders = ParseCsvLine(headerLine);
                fileHeaders = splitHeaders;
                // Remove support for different order: just check for equality
                if (fileHeaders.Count != adapter.Headers.Count)
                {
                    throw new IOException($"Header count mismatch in file '{filePath}'.");
                }
                bool headersMatch = true;
                for (int i = 0; i < fileHeaders.Count; i++)
                {
                    if (!string.Equals(fileHeaders[i], adapter.Headers[i], StringComparison.OrdinalIgnoreCase))
                    {
                        headersMatch = false;
                        break;
                    }
                }
                if (!headersMatch)
                {
                    throw new IOException($"Header mismatch in file '{filePath}'. Headers must match exactly the adapter headers and order.");
                }
            }
        }
        else
        {
            yield break;
        }
        while (!reader.EndOfStream && !cancellationToken.IsCancellationRequested)
        {
            string line = null;
            try
            {
                line = await reader.ReadLineAsync();
            }
            catch (IOException ex)
            {
                throw new IOException($"Error reading line from file '{filePath}': {ex.Message}", ex);
            }
            if (!string.IsNullOrWhiteSpace(line))
            {
                var fields = ParseCsvLine(line);
                if (fields.Count != fileHeaders.Count)
                {
                    throw new IOException($"Field count mismatch in file '{filePath}' at line: {line}");
                }
                yield return adapter.FromLine(fields);
            }
        }
    }
}
