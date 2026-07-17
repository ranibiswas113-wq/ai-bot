# AI Trading Bot for Quotex

An AI-powered trading bot that uses moving average crossover strategy to generate buy/sell signals for Quotex trading platform.

## Features

- **Moving Average Crossover Strategy**: Uses 10-period and 20-period moving averages
- **Signal Generation**: Automatic BUY/SELL/WAIT signals based on MA crossovers
- **Quotex Integration**: Ready to connect with Quotex API
- **Real-time Data**: Fetches and analyzes market data continuously

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ranibiswas113-wq/ai-bot.git
cd ai-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Quotex credentials:
```
QUOTEX_EMAIL=your_email@example.com
QUOTEX_PASSWORD=your_password
```

## Usage

Run the bot:
```bash
python main.py
```

## Strategy Details

The bot uses a **Moving Average Crossover (MAC)** strategy:

- **Fast MA**: 10-period moving average (short-term trend)
- **Slow MA**: 20-period moving average (long-term trend)

### Signals:
- **BUY**: Fast MA > Slow MA (bullish crossover)
- **SELL**: Fast MA < Slow MA (bearish crossover)
- **WAIT**: No clear signal

## Files

- `strategy.py`: Trading strategy implementation
- `main.py`: Main bot execution file
- `config.py`: Configuration settings
- `requirements.txt`: Python dependencies

## Disclaimer

⚠️ **Risk Warning**: Trading involves substantial risk. This bot is for educational purposes only. Always use risk management and never trade with money you cannot afford to lose.

## License

MIT License
