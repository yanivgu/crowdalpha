using System.Collections.Generic;

namespace SentimentAnalyzer.Domain;

public class SentimentAnalysisResponse
{
    public SentimentAnalysisRequest Request { get; set; }
    public Dictionary<string, int> SentimentScores { get; set; }
}
