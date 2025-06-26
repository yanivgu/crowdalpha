using System.Collections.Generic;
using System.Threading.Tasks;

namespace SentimentAnalyzer.Domain;

public interface ISentimentAnalysisService
{
    Task<SentimentAnalysisResponse> AnalyzeAsync(SentimentAnalysisRequest request);
    IAsyncEnumerable<SentimentAnalysisResponse> AnalyzeAsync(List<SentimentAnalysisRequest> requests);
}
