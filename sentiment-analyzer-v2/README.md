# Sentiment Analyzer v2

## Overview
Sentiment Analyzer v2 is a .NET solution designed to analyze the sentiment of social network posts, particularly for financial and stock market applications. The solution is organized into multiple projects following a clean architecture approach, separating concerns into Application, Domain, and Infrastructure layers.

## Projects
- **SentimentAnalyzer**: Main entry point and orchestration.
- **SentimentAnalyzer.Application**: Application logic, use cases, and service interfaces.
- **SentimentAnalyzer.Domain**: Core business logic and domain entities.
- **SentimentAnalyzer.Infrastructure**: Data access, external services, and implementation details.

## Features
- Sentiment analysis of social media posts.
- Modular and extensible architecture.
- Designed for financial data and stock market sentiment.

## Getting Started
1. **Requirements:**
   - .NET 6.0 SDK or later
   - Visual Studio 2022 or later (recommended)

2. **Build and Run:**
   - Open `sentiment-analyzer-v2.sln` in Visual Studio.
   - Restore NuGet packages.
   - Set `SentimentAnalyzer` as the startup project.
   - Build and run the solution.

3. **Configuration:**
   - Update configuration files as needed for data sources and output paths.

## Folder Structure
- `SentimentAnalyzer/` - Main application
- `SentimentAnalyzer.Application/` - Application layer
- `SentimentAnalyzer.Domain/` - Domain layer
- `SentimentAnalyzer.Infrastructure/` - Infrastructure layer

## Sample Input
Example of a social posts input CSV:

```csv
OwnerID,MessageText,CreateTime
14089249,$NVDA  Earnings?,2024-02-21 12:14:37.000000
10604032,🎯💰💵 $meta $AMZN $GOOG ,2025-01-03 23:21:57.705000
10604032,"Feb 26, 2025  💥 Big Movers in our Portfolio  🎯 $AXON  🚀 $SMCI  📈 $ENR.DE  💵 $VST  💰 $1810.HK   ✨ Join our Trading Community 💡Start copying @Traderbulgfab   💵💰 Return 1Y +26.66% ⚖️ Low Risk Score 4 🌟 long-term investments 📈 dividends reinvested in new stocks  🚧 no cryptocurrencies 🚧 no leverage 🚧 no short selling  📣 How to get started: https://www.etoro.com/copytrader/ ",2025-02-26 21:08:28.653000
```

## Sample Output
Example of a sentiment output CSV:

```csv
OwnerID,CreateTime,PlayerLevel,TwoYearGain,MonthsActive,Symbol,SentimentScore
14089249,2024-02-21T12:14:37.0000000,Platinum Plus,216.79,61,NVDA,0
10604032,2025-01-03T23:21:57.7050000,Gold,29.19,39,AMZN,0
10604032,2025-01-03T23:21:57.7050000,Gold,29.19,39,GOOG,0
10604032,2025-02-26T21:08:28.6530000,Gold,29.19,39,AXON,1
```

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements.

## License
This project is for educational and research purposes.
