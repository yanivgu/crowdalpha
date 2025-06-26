using System;

namespace SentimentAnalyzer.Domain.DTOs
{
    public class UserData
    {
        public int UserId { get; set; }
        public string Level { get; set; }
        public int MonthsActive { get; set; }
        public decimal TwoYearGain { get; set; }
    }
}
