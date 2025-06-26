using SentimentAnalyzer.Domain;
using System;
using System.IO;

namespace SentimentAnalyzer.Infrastructure;

public class FileLogger : ILogger, IDisposable
{
    private readonly string _filePath;
    private readonly object _lock = new();
    private StreamWriter _writer;

    public FileLogger(string filePath)
    {
        _filePath = filePath;
        _writer = new StreamWriter(_filePath, append: true) { AutoFlush = true };
    }

    private void Log(string level, string message)
    {
        var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
        lock (_lock)
        {
            _writer.WriteLine($"[{timestamp}] [{level}] {message}");
        }
    }

    public void Debug(string message) => Log("DEBUG", message);
    public void Info(string message) => Log("INFO", message);
    public void Warn(string message) => Log("WARN", message);
    public void Error(string message) => Log("ERROR", message);

    public void Dispose()
    {
        lock (_lock)
        {
            _writer?.Dispose();
            _writer = null;
        }
    }
}
