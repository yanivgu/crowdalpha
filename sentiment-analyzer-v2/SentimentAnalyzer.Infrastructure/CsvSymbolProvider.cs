using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

using SentimentAnalyzer.Domain;

namespace SentimentAnalyzer.Infrastructure;

public class CsvSymbolProvider : ISymbolProvider
{
    private readonly string _csvFilePath;
    private HashSet<string> _symbols;
    private bool _loaded;
    private static readonly SemaphoreSlim _semaphore = new SemaphoreSlim(1, 1);
    private readonly CsvTextFileReader _fileReader;
    private readonly ILogger _logger;

    public CsvSymbolProvider(CsvTextFileReader fileReader, string csvFilePath, ILogger logger)
    {
        _fileReader = fileReader;
        _csvFilePath = csvFilePath;
        _symbols = new HashSet<string>();
        _loaded = false;
        _logger = logger;
    }

    private async Task EnsureLoadedAsync()
    {
        if (_loaded) return;
        await _semaphore.WaitAsync();
        try
        {
            if (_loaded) return;
            await foreach (var symbol in _fileReader.ReadLinesAsync(_csvFilePath, CsvSymbolsFileAdapter.Instance))
            {
                if (!string.IsNullOrEmpty(symbol))
                    _symbols.Add(symbol.ToUpperInvariant());
            }
            _loaded = true;
            _logger.Info($"Loaded {_symbols.Count} symbols from CSV file: {_csvFilePath}");
        }
        finally
        {
            _semaphore.Release();
        }
    }

    public async Task<HashSet<string>> GetAllSymbolsAsync()
    {
        await EnsureLoadedAsync();
        return new HashSet<string>(_symbols);
    }

    public async Task<string> GetSymbolAsync(string symbol)
    {
        await EnsureLoadedAsync();
        return _symbols.Contains(symbol.ToUpperInvariant()) ? symbol : null;
    }

    private class CsvSymbolsFileAdapter : ICsvAdapter<string>
    {
        public static readonly CsvSymbolsFileAdapter Instance = new CsvSymbolsFileAdapter();
        private static readonly IReadOnlyList<string> _headers = new List<string> { "Symbol" };
        public IReadOnlyList<string> Headers => _headers;

        public string FromLine(IReadOnlyList<string> fields)
        {
            if (fields.Count != 1) throw new ArgumentException("Invalid fields");
            return fields[0];
        }

        public IReadOnlyList<string> ToLines(string obj)
        {
            throw new NotImplementedException();
        }
    }
}
