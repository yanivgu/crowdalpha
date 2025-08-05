# CrowdAlpha

CrowdAlpha is a comprehensive financial sentiment analysis and portfolio optimization system that leverages social media sentiment from financial social networks to create and optimize investment portfolios. The project combines AI-powered sentiment analysis with quantitative portfolio simulation to explore the relationship between crowd sentiment and market performance.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Data Pipeline](#data-pipeline)
- [Usage](#usage)
- [Sample Data](#sample-data)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

CrowdAlpha explores whether sentiment from financial social media posts can be used to create profitable investment strategies. The system:

1. **Analyzes sentiment** from social media posts mentioning stock symbols using Azure OpenAI
2. **Processes and enriches** the sentiment data with user characteristics and temporal features
3. **Simulates portfolio performance** using sentiment-based scoring algorithms
4. **Optimizes portfolio weights** through unsupervised learning techniques
5. **Compares performance** against market benchmarks like the S&P 500

## 📁 Project Structure

```
crowdalpha/
├── sentiment-analyzer-v2/          # .NET sentiment analysis engine
│   ├── SentimentAnalyzer/           # Main application entry point
│   ├── SentimentAnalyzer.Application/ # Application logic layer
│   ├── SentimentAnalyzer.Domain/    # Domain entities and interfaces
│   └── SentimentAnalyzer.Infrastructure/ # External services and data access
├── scripts/                        # Data processing and utility scripts
│   ├── build ml dataset/           # ML dataset construction
│   ├── historical prices/          # Stock price data collection
│   ├── process sentiments/         # Sentiment data processing
│   ├── symbol daily gains/         # Daily return calculations
│   └── ticker parser/              # Stock symbol extraction
├── ml/                             # Machine learning and portfolio optimization
│   ├── modular_portfolio/          # Portfolio simulation engine
│   └── visualize/                  # Performance visualization tools
├── data/                           # Data storage and samples
│   └── samples/                    # Sample datasets for testing
└── docs/                           # Documentation and project artifacts
```

## ✨ Key Features

### Sentiment Analysis Engine (.NET)
- **Azure OpenAI Integration**: Uses GPT models for sophisticated sentiment analysis
- **Stock Symbol Extraction**: Automatically identifies and validates stock symbols in posts
- **User Context Enrichment**: Incorporates user performance data and trading experience
- **Scalable Processing**: Parallel processing with configurable concurrency
- **Clean Architecture**: Separation of concerns with Domain-Driven Design

### Data Processing Pipeline (Python)
- **Multi-source Data Integration**: Combines sentiment, price, and user data
- **Temporal Feature Engineering**: Creates time-based features like days since post
- **Data Quality Assurance**: Handles missing values and data validation
- **Statistical Analysis**: Generates comprehensive dataset statistics

### Portfolio Optimization System
- **Sentiment Scoring**: Converts raw sentiment into actionable investment signals
- **Multi-factor Weighting**: Considers user credibility, sentiment strength, and recency
- **Portfolio Simulation**: Backtests strategies with configurable parameters
- **Performance Metrics**: Calculates returns, drawdowns, and risk metrics
- **Benchmark Comparison**: Compares against S&P 500 performance

## 🛠️ Technologies Used

### Backend & Analysis
- **.NET 6.0+** - Sentiment analysis engine
- **Azure OpenAI** - Large language model for sentiment analysis
- **Python 3.x** - Data processing and machine learning
- **pandas & numpy** - Data manipulation and numerical computing
- **matplotlib** - Data visualization

### Data & Infrastructure
- **CSV-based data pipeline** - Flexible and portable data storage
- **Parallel processing** - Efficient handling of large datasets
- **Configuration-driven** - Easy customization via config files

## 🚀 Getting Started

### Prerequisites

#### For Sentiment Analysis (.NET)
- .NET 6.0 SDK or later
- Visual Studio 2022 or JetBrains Rider (recommended)
- Azure OpenAI API access and credentials

#### For Data Processing & ML (Python)
- Python 3.8+
- Required packages: `pandas`, `numpy`, `matplotlib`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yanivgu/crowdalpha.git
   cd crowdalpha
   ```

2. **Set up the .NET sentiment analyzer**
   ```bash
   cd sentiment-analyzer-v2
   dotnet restore
   ```
   
   Configure your Azure OpenAI settings in `appsettings.json`:
   ```json
   {
     "AzureOpenAI": {
       "Endpoint": "your-endpoint-url",
       "Deployment": "your-deployment-name",
       "ApiKey": "your-api-key"
     }
   }
   ```

3. **Set up Python environment**
   ```bash
   pip install pandas numpy matplotlib
   ```

## 🔄 Data Pipeline

The CrowdAlpha system processes data through several stages:

### 1. Sentiment Analysis
```bash
cd sentiment-analyzer-v2
dotnet run --project SentimentAnalyzer
```
- Processes social media posts from CSV files
- Extracts stock symbols and analyzes sentiment
- Enriches with user performance data
- Outputs structured sentiment scores

### 2. Data Processing
```bash
cd scripts/process\ sentiments/
python process_sentiments.py
```
- Cleans and structures sentiment data
- Adds temporal features (days since post)
- Maps user levels to numeric IDs

### 3. Dataset Construction
```bash
cd scripts/build\ ml\ dataset/
python build_ml_dataset.py --save-stats
```
- Merges sentiment data with daily price gains
- Creates unified ML dataset
- Generates statistical summaries

### 4. Portfolio Simulation
```bash
cd ml/modular_portfolio/
python main.py path/to/sentiments_processed.csv path/to/prices_agg.csv
```
- Simulates portfolio performance using sentiment scores
- Optimizes weights through unsupervised learning
- Generates performance reports and visualizations

## 📊 Sample Data

The repository includes sample datasets for testing and understanding:

- **`sample_AAPL_historical.csv`** - Historical price data for Apple Inc.
- **`sample_sentiments_output.csv`** - Processed sentiment analysis results
- **`sample_social_posts.csv`** - Raw social media posts data
- **`sample_gains.csv`** - Daily stock return calculations

### Sample Sentiment Output Format
```csv
OwnerID,CreateTime,PlayerLevel,TwoYearGain,MonthsActive,Symbol,SentimentScore
14089249,2024-02-21T12:14:37.0000000,Platinum Plus,216.79,61,NVDA,0
10604032,2025-01-03T23:21:57.7050000,Gold,29.19,39,AMZN,0
10604032,2025-02-26T21:08:28.6530000,Gold,29.19,39,AXON,1
```

## 📈 Results

Based on the portfolio simulation results:

### Performance Summary
| Strategy | Total Gain | Max Drawdown | Symbols Used |
|----------|------------|--------------|--------------|
| **Optimized Portfolio** | 26.70% | 16.10% | Top 10 stocks |
| **Equal Weight Baseline** | 16.21% | 17.81% | Top 10 stocks |
| **S&P 500 Benchmark** | ~15-20%* | ~12-18%* | 500 stocks |

*Note: Benchmark performance varies by time period

### Key Findings
- **Sentiment-based strategies** can outperform simple baseline approaches
- **User credibility weighting** (based on trading performance) improves results
- **Optimal portfolio size** appears to be around 10-15 stocks
- **Drawdown management** is crucial for risk-adjusted returns

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines
1. Follow the existing code style and architecture patterns
2. Add tests for new features when applicable
3. Update documentation for any new functionality
4. Ensure all scripts run successfully with sample data

## 📄 License

This project is for educational and research purposes. Please see the individual component licenses for more details.

## 📚 Additional Resources

- **Documentation**: See the `/docs` folder for detailed project documentation
- **Individual Component READMEs**: Each major component has its own README with specific usage instructions
- **Sample Configurations**: Example configuration files are provided for easy setup

---

**Note**: This is a research project exploring the intersection of social sentiment and financial markets. Results should not be considered as investment advice.
