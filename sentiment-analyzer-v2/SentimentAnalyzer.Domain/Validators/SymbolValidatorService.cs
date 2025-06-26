using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace SentimentAnalyzer.Domain;

public class SymbolValidatorService : ISymbolValidatorService
{
    private readonly ISymbolProvider _symbolProvider;

    public SymbolValidatorService(ISymbolProvider symbolProvider)
    {
        _symbolProvider = symbolProvider;
    }

    public async Task<SymbolValidationResult> ValidateAsync(string text)
    {
        var allSymbols = await _symbolProvider.GetAllSymbolsAsync();
        var foundSymbols = ExtractSymbols(text);
        var relevantSymbols = foundSymbols.Where(s => allSymbols.Contains(s.ToUpper())).ToList();

        return new SymbolValidationResult
        {
            SymbolsFound = foundSymbols,
            RelevantSymbols = relevantSymbols
        };
    }

    private List<string> ExtractSymbols(string text)
    {
        var matches = Regex.Matches(text, @"\$([A-Za-z0-9]+\.?[A-Z]+)");
        return matches.Select(m => m.Groups[1].Value).Distinct().ToList();
    }
}
