using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using SentimentAnalyzer.Domain;

namespace SentimentAnalyzer.Infrastructure;

public class CsvTextFileWriter
{
    private readonly ILogger _logger;
    public CsvTextFileWriter(ILogger logger = null) { _logger = logger; }

    public async Task WriteLinesAsync<T>(IAsyncEnumerable<T> items, ICsvAdapter<T> adapter, string filePath, CancellationToken cancellationToken = default)
    {
        try
        {
            using var stream = new FileStream(filePath, FileMode.Create, FileAccess.Write, FileShare.None, 4096, true);
            using var writer = new StreamWriter(stream);
            // Write header
            await writer.WriteLineAsync(string.Join(",", adapter.Headers));
            await writer.FlushAsync();
            await foreach (var item in items.WithCancellation(cancellationToken))
            {
                try
                {
                    var lines = adapter.ToLines(item);
                    foreach (var line in lines)
                    {
                        await writer.WriteLineAsync(line);
                    }
                    await writer.FlushAsync();
                }
                catch (IOException ex)
                {
                    throw new IOException($"Error writing line to file '{filePath}': {ex.Message}", ex);
                }
            }
        }
        catch (IOException)
        {
            throw;
        }
        catch (UnauthorizedAccessException ex)
        {
            throw new IOException($"Access denied to file '{filePath}': {ex.Message}", ex);
        }
        catch (Exception ex)
        {
            throw new IOException($"Error writing to file '{filePath}': {ex.Message}", ex);
        }
    }
}
