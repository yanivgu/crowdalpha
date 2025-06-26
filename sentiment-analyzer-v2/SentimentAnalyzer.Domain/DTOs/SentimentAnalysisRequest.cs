using System;

namespace SentimentAnalyzer.Domain;

public class SentimentAnalysisRequest
{
    public int OwnerId { get; set; }
    public string MessageText { get; set; }
    public DateTime CreateTime { get; set; }
    public string PlayerLevel { get; set; }
    public decimal TwoYearGain { get; set; }
    public int MonthsActive { get; set; }
}
