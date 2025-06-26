using SentimentAnalyzer.Domain.DTOs;
using System;
using System.Collections.Generic;
using SentimentAnalyzer.Infrastructure;

namespace SentimentAnalyzer;

public class SentimentAnalysisRequestCsvAdapter : ICsvAdapter<SocialPostData>
{
    public IReadOnlyList<string> Headers => new[] { "OwnerId", "MessageText", "CreateTime" };

    public SocialPostData FromLine(IReadOnlyList<string> fields)
    {
        if (fields.Count != 3)
            throw new ArgumentException("Invalid number of fields for SocialPostData");
        return new SocialPostData
        {
            OwnerId = int.TryParse(fields[0], out var ownerId) ? ownerId : 0,
            MessageText = fields[1],
            CreateTime = DateTime.TryParse(fields[2], out var createTime) ? createTime : default
        };
    }

    public IReadOnlyList<string> ToLines(SocialPostData obj)
    {
        throw new NotImplementedException();
    }
}
