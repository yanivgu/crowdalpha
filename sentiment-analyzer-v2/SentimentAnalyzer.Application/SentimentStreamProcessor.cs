using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using SentimentAnalyzer.Application;
using SentimentAnalyzer.Domain;

namespace SentimentAnalyzer.Infrastructure;

public class SentimentStreamProcessor
{
    private readonly SentimentAnalysisService _sentimentService;
    private readonly int _maxDegreeOfParallelism;
    private readonly SemaphoreSlim _semaphore;

    public SentimentStreamProcessor(SentimentAnalysisService sentimentService, int maxDegreeOfParallelism = 5)
    {
        _sentimentService = sentimentService;
        _maxDegreeOfParallelism = maxDegreeOfParallelism;
        _semaphore = new SemaphoreSlim(maxDegreeOfParallelism);
    }

    public async IAsyncEnumerable<SentimentAnalysisResponse> Process(
        IAsyncEnumerable<SentimentAnalysisRequest> source,
        [System.Runtime.CompilerServices.EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        int processedCount = 0;    
    
        await foreach (var request in source.WithCancellation(cancellationToken))
        {
            try
            {
                await _semaphore.WaitAsync(cancellationToken);
                yield return await _sentimentService.AnalyzeAsync(request);
                processedCount++;
                if (processedCount % 100 == 0)
                {
                    Console.WriteLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}] Processed {processedCount} requests...");
                }
            }
            finally
            {
                _semaphore.Release();
            }
        }
    }
}
