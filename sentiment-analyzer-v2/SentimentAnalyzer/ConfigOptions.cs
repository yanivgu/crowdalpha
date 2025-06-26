namespace SentimentAnalyzer.Config
{
    public class AzureOpenAIOptions
    {
        public string Endpoint { get; set; }
        public string Deployment { get; set; }
        public string ApiKey { get; set; }
    }
    public class FilePathsOptions
    {
        public string SpxCompanies { get; set; }
        public string SocialPostsOwners { get; set; }
        public string SocialPostsMessages { get; set; }
        public string Gains { get; set; }
        public string Output { get; set; }
    }
    public class LoggingOptions
    {
        public LogFilePrefixOptions LogFilePrefix { get; set; }
    }
    public class LogFilePrefixOptions
    {
        public string Value { get; set; }
    }
    public class AnalyzerOptions
    {
        public int MaxDegreeOfParallelism { get; set; } = 5;
        public int MaxAbsSentiment { get; set; } = 2;
    }
}
