using SentimentAnalyzer.Domain;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

namespace SentimentAnalyzer.Application;

public class SentimentAnalysisService : ISentimentAnalysisService
{
    private readonly IAzureOpenAIClientService _openAIClientService;
    private readonly ISymbolValidatorService _symbolValidatorService;
    private readonly ILogger _logger;
    private readonly int _maxAbsSentiment;
    private string SystemPrompt =>
        $"You are a financial sentiment analyzer. " +
        $"Analyze the sentiment of the following text and provide a numerical score for the sentiment towards each stock symbol mentioned in the post. " +
        $"All stock symbols begin with $ sign. If a stock symbol is not mentioned, do not provide a score for it. " +
        $"The score should be between -{_maxAbsSentiment} (very negative) and {_maxAbsSentiment} (very positive). " +
        $"If the sentiment is neutral, return a score of 0. " +
        $"The sentiment should reflect the overall tone of the text towards the stock symbols, not just the presence of the symbol. " +
        $"For example, if the text is 'I think $AAPL is a great company', the score for AAPL should be positive. " +
        $"If the text is 'I don't like $GOOGL', the score for GOOGL should be negative. " +
        $"If the text is 'What do you think about $AMZN?', the score for AMZN should be neutral (0). " +
        $"Differentiate between opinionated and reasoned sentiment, versus general questions about the market behaviour. " +
        $"If the text contains multiple symbols, provide a score for each symbol mentioned. " +
        $"The difference between a low positive score (1) and a high positive score ({_maxAbsSentiment}) should be based on the strength of the sentiment expressed in the text and the reasoning behind it. " +
        $"For example, if the text is 'I think $AAPL is a great company because of its strong earnings', the score for AAPL should be higher than if the text is simply 'I like $AAPL'. " +
        $"Detailed analysis of a company's performance, market trends, and other relevant factors should be considered in the sentiment analysis scores. " +
        $"Provide the scores in a JSON dictionary format with the stock symbols without $ as keys and the sentiment scores as integer values. " +
        $"Respond only with the JSON dictionary. For example: {{ \"AAPL\": 2, \"GOOGL\": -1, \"AMZN\": 0 }}.";

    public SentimentAnalysisService(
        IAzureOpenAIClientService openAIClientService,
        ISymbolValidatorService symbolValidatorService,
        ILogger logger,
        int maxAbsSentiment = 2)
    {
        _openAIClientService = openAIClientService;
        _symbolValidatorService = symbolValidatorService;
        _logger = logger;

        if (maxAbsSentiment <= 1)
            _logger.Warn("maxAbsSentiment should be greater than 1. Setting it to 2.");
        _maxAbsSentiment = Math.Max(maxAbsSentiment, 2);
        _openAIClientService.SetSystemPrompt(SystemPrompt);
    }

    public async Task<SentimentAnalysisResponse> AnalyzeAsync(SentimentAnalysisRequest request)
    {
        return await this.AnalyzeAsync(new List<SentimentAnalysisRequest> { request }).FirstOrDefaultAsync();
    }

    public async IAsyncEnumerable<SentimentAnalysisResponse> AnalyzeAsync(List<SentimentAnalysisRequest> requests)
    {
        foreach (var request in requests)
        {
            var validationResult = await _symbolValidatorService.ValidateAsync(request.MessageText);
            if (!validationResult.HasRelevantSymbol)
            {
                continue;
            }
            string responseJson = null;
            try
            {
                responseJson = await _openAIClientService.AnalyzeSentimentAsync(SystemPrompt, request.MessageText);
            }
            catch (Exception ex)
            {
                _logger.Error($"Exception during sentiment analysis for message: \"{request.MessageText}\"");
                _logger.Error($"Exception: {ex}");
                continue;
            }
            yield return ParseResponse(responseJson, request, validationResult);
        }
    }

    private SentimentAnalysisResponse ParseResponse(string json, SentimentAnalysisRequest request, SymbolValidationResult validationResult)
    {
        var sanitized_json = SanitizeJsonResponse(json);
        Dictionary<string, int> dict = null;
        try
        {
            dict = JsonSerializer.Deserialize<Dictionary<string, int>>(sanitized_json);
        }
        catch (Exception ex)
        {
            _logger.Error($"Error parsing sentiment response. Response content:\n{json}\nSanitized content:\n{sanitized_json}");
            _logger.Error($"Exception: {ex}");
        }
        dict = dict.Where(kvp => validationResult.RelevantSymbols.Contains(kvp.Key))
                .ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
        return new SentimentAnalysisResponse { Request = request, SentimentScores = dict ?? new() };
    }

    private string SanitizeJsonResponse(string response)
    {
        if (string.IsNullOrWhiteSpace(response))
            return "{}";

        int firstBracket = response.IndexOf('{');
        int lastBracket = response.LastIndexOf('}');
        if (firstBracket == -1 || lastBracket == -1 || lastBracket < firstBracket)
            return "{}";

        return response.Substring(firstBracket, lastBracket - firstBracket + 1);
    }
}
