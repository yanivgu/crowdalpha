using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;
using SentimentAnalyzer.Config;

namespace SentimentAnalyzer;

public class Program
{
    public static async Task Main(string[] args)
    {
        var configuration = new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .Build();

        var services = new ServiceCollection();
        services.Configure<AzureOpenAIOptions>(configuration.GetSection("AzureOpenAI"));
        services.Configure<FilePathsOptions>(configuration.GetSection("FilePaths"));
        services.Configure<LoggingOptions>(configuration.GetSection("Logging"));
        services.Configure<AnalyzerOptions>(configuration.GetSection("Analyzer"));
        services.AddSingleton<llmSentimentAnalyzer>();
        services.AddSingleton<IConfiguration>(configuration);
        var provider = services.BuildServiceProvider();

        var analyzer = provider.GetRequiredService<llmSentimentAnalyzer>();
        analyzer.Init();

        var filePaths = provider.GetRequiredService<IOptions<FilePathsOptions>>().Value;
        string sourceCsv = filePaths.SocialPostsMessages;
        string destinationCsv = string.Format(filePaths.Output, DateTime.Now);
        await analyzer.ExecuteAsync(sourceCsv, destinationCsv);
    }
}
