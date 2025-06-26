using SentimentAnalyzer.Domain;
using System;

namespace SentimentAnalyzer.Infrastructure;

public class ConsoleLogger : ILogger
{
    private void Log(string level, string message)
    {
        var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
        Console.WriteLine($"[{timestamp}] [{level}] {message}");
    }

    public void Debug(string message) => Log("DEBUG", message);
    public void Info(string message) => Log("INFO", message);
    public void Warn(string message) => Log("WARN", message);
    public void Error(string message) => Log("ERROR", message);
}
