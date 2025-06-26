using System.Collections.Generic;

namespace SentimentAnalyzer.Domain;

public class SymbolValidationResult
{
    public List<string> SymbolsFound { get; set; } = new();
    public List<string> RelevantSymbols { get; set; } = new();
    public int SymbolsFoundCount => SymbolsFound.Count;
    public int RelevantSymbolsCount => RelevantSymbols.Count;
    public bool HasRelevantSymbol => RelevantSymbolsCount >= 1;
}
