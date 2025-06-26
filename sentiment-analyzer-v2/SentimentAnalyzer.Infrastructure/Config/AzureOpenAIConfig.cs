using System;

namespace SentimentAnalyzer.Infrastructure;

public class AzureOpenAIConfig
{
    public AzureOpenAIConfig(string endpoint, string deploymentName, string apiKey)
    {
        Endpoint = new Uri(endpoint);
        DeploymentName = deploymentName;
        ApiKey = apiKey;
    }

    public AzureOpenAIConfig() { }

    public Uri Endpoint { get; set; }
    public string DeploymentName { get; set; }
    public string ApiKey { get; set; }
}
