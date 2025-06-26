using SentimentAnalyzer.Domain;
using System;
using System.Collections.Generic;
using System.Linq;
using SentimentAnalyzer.Infrastructure;

namespace SentimentAnalyzer;

public class SentimentAnalysisResponseCsvAdapter : ICsvAdapter<SentimentAnalysisResponse>
{
    public IReadOnlyList<string> Headers => new[] { "OwnerID", "CreateTime", "PlayerLevel", "TwoYearGain", "MonthsActive", "Symbol", "SentimentScore" };

    public SentimentAnalysisResponse FromLine(IReadOnlyList<string> fields)
    {
        throw new NotImplementedException();
    }

    public IReadOnlyList<string> ToLines(SentimentAnalysisResponse obj)
    {
        var lines = new List<string>();
        if (obj?.SentimentScores != null && obj.SentimentScores.Count > 0 && obj.Request != null)
        {
            foreach (var kvp in obj.SentimentScores)
            {
                var ownerId = obj.Request?.OwnerId.ToString() ?? string.Empty;
                var createTime = obj.Request?.CreateTime.ToString("o") ?? string.Empty;
                var playerLevel = obj.Request?.PlayerLevel ?? string.Empty;
                var twoYearGain = obj.Request?.TwoYearGain.ToString() ?? string.Empty;
                var monthsActive = obj.Request?.MonthsActive.ToString() ?? string.Empty;
                var symbol = kvp.Key ?? string.Empty;
                var sentimentScore = kvp.Value.ToString();

                var line = string.Join(",", new[]
                {
                    ownerId,
                    createTime,
                    playerLevel,
                    twoYearGain,
                    monthsActive,
                    symbol,
                    sentimentScore
                });
                lines.Add(line);
            }
        }
        return lines;
    }
}
