using System.Threading.Tasks;

namespace SentimentAnalyzer.Domain;

public interface IAzureOpenAIClientService
{
    void SetSystemPrompt(string systemPrompt);
    Task<string> AnalyzeSentimentAsync(string systemPrompt, string userText);
}
