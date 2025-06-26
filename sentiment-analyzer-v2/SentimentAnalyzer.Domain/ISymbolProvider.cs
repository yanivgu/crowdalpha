using System.Collections.Generic;
using System.Threading.Tasks;

namespace SentimentAnalyzer.Domain;

public interface ISymbolProvider
{
    Task<HashSet<string>> GetAllSymbolsAsync();
    Task<string> GetSymbolAsync(string symbol);
}
