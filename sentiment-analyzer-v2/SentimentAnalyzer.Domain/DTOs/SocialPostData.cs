using System;

namespace SentimentAnalyzer.Domain.DTOs
{
    public class SocialPostData
    {
        public int OwnerId { get; set; }
        public string MessageText { get; set; }
        public DateTime CreateTime { get; set; }
    }
}
