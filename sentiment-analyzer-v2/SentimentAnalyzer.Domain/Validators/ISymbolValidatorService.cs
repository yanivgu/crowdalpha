using System.Threading.Tasks;

namespace SentimentAnalyzer.Domain;

public interface ISymbolValidatorService
{
    Task<SymbolValidationResult> ValidateAsync(string text);
}
