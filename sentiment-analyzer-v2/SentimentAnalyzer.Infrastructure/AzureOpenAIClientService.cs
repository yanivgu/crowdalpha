using System.Collections.Generic;
using System.Threading.Tasks;
using Azure;
using Azure.AI.OpenAI;
using OpenAI.Chat;
using SentimentAnalyzer.Domain;

namespace SentimentAnalyzer.Infrastructure;

public class AzureOpenAIClientService : IAzureOpenAIClientService
{
    private readonly AzureOpenAIConfig _config;
    private readonly AzureOpenAIClient _client;
    private readonly ChatClient _chatClient;
    string SystemPrompt { get; set; }

    public AzureOpenAIClientService(AzureOpenAIConfig config, string systemPrompt)
    {
        SystemPrompt = systemPrompt;
        _config = config;
        _client = new AzureOpenAIClient(_config.Endpoint, new AzureKeyCredential(_config.ApiKey));
        _chatClient = _client.GetChatClient(_config.DeploymentName);
    }

    public void SetSystemPrompt(string systemPrompt)
    {
        SystemPrompt = systemPrompt;
    }

    public async Task<string> AnalyzeSentimentAsync(string systemPrompt, string userText)
    {
        var requestOptions = new ChatCompletionOptions
        {
            MaxOutputTokenCount = 4096,
            Temperature = 0.0f, // expect a deterministic response
            TopP = 1.0f,
        };

        List<ChatMessage> messages = new List<ChatMessage>
        {
            new SystemChatMessage(systemPrompt),
            new UserChatMessage(userText),
        };

        var response = await _chatClient.CompleteChatAsync(messages, requestOptions);
        return response.Value.Content[0].Text;
    }
}
