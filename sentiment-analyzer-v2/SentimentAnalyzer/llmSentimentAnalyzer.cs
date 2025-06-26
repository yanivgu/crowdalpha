using Microsoft.Extensions.Options;
using SentimentAnalyzer.Application;
using SentimentAnalyzer.Config;
using SentimentAnalyzer.Domain;
using SentimentAnalyzer.Domain.DTOs;
using SentimentAnalyzer.Infrastructure;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Threading;

namespace SentimentAnalyzer;

public class llmSentimentAnalyzer
{
    private SentimentAnalysisService sentimentService;
    private CsvTextFileReader fileReader;
    private CsvTextFileWriter fileWriter;
    private SentimentStreamProcessor streamProcessor;
    private IUserDataProvider userDataProvider;
    private ILogger _logger;

    private AzureOpenAIOptions _openAIOptions;
    private FilePathsOptions _filePathsOptions;
    private LoggingOptions _loggingOptions;
    private AnalyzerOptions _analyzerOptions;

    public llmSentimentAnalyzer(
        IOptions<AzureOpenAIOptions> openAIOptions,
        IOptions<FilePathsOptions> filePathsOptions,
        IOptions<LoggingOptions> loggingOptions,
        IOptions<AnalyzerOptions> analyzerOptions)
    {
        _openAIOptions = openAIOptions.Value;
        _filePathsOptions = filePathsOptions.Value;
        _loggingOptions = loggingOptions.Value;
        _analyzerOptions = analyzerOptions.Value;
    }

    public void Init()
    {
        _logger = new FileLogger($"{_loggingOptions.LogFilePrefix.Value}{DateTime.Now:yyyyMMdd}.log");
        var config = new AzureOpenAIConfig(
            _openAIOptions.Endpoint,
            _openAIOptions.Deployment,
            _openAIOptions.ApiKey
        );
        var openAIService = new AzureOpenAIClientService(config, "");
        fileReader = new CsvTextFileReader(_logger);
        fileWriter = new CsvTextFileWriter();
        var symbolProvider = new CsvSymbolProvider(fileReader, _filePathsOptions.SpxCompanies, _logger);
        var symbolValidator = new SymbolValidatorService(symbolProvider);
        sentimentService = new SentimentAnalysisService(
            openAIService,
            symbolValidator,
            _logger,
            _analyzerOptions.MaxAbsSentiment
        );
        streamProcessor = new SentimentStreamProcessor(sentimentService, _analyzerOptions.MaxDegreeOfParallelism);
        userDataProvider = new CsvUserDataProvider(
            fileReader,
            _filePathsOptions.SocialPostsOwners,
            _filePathsOptions.Gains,
            _logger
        );
    }

    public async Task ExecuteAsync(string sourceCsv, string destCsv, CancellationToken cancellationToken = default)
    {
        var requestAdapter = new SentimentAnalysisRequestCsvAdapter();
        var responseAdapter = new SentimentAnalysisResponseCsvAdapter();
        await userDataProvider.InitAsync();
        var sourceStream = fileReader.ReadLinesAsync<SocialPostData>(sourceCsv, requestAdapter, cancellationToken);
        var enrichedStream = EnrichWithUserData(sourceStream, userDataProvider);
        var processedStream = streamProcessor.Process(enrichedStream, cancellationToken);
        await fileWriter.WriteLinesAsync(processedStream, responseAdapter, destCsv, cancellationToken);
    }

    private async IAsyncEnumerable<SentimentAnalysisRequest> EnrichWithUserData(IAsyncEnumerable<SocialPostData> posts, IUserDataProvider userDataProvider)
    {
        await foreach (var post in posts)
        {
            var userData = await userDataProvider.GetUserDataAsync(post.OwnerId);
            if (userData == null) continue;
            yield return new SentimentAnalysisRequest
            {
                OwnerId = post.OwnerId,
                MessageText = post.MessageText,
                CreateTime = post.CreateTime,
                PlayerLevel = userData.Level,
                TwoYearGain = userData.TwoYearGain,
                MonthsActive = userData.MonthsActive
            };
        }
    }
}
