# Strategy Builder

An AI-powered trading strategy generator that converts plain English descriptions into executable Python code and backtests them against real market data.

![Demo](demo.gif)

## Features

- **Natural Language to Code**: Describe your trading strategy in plain English, get working Python code
- **RAG-Enhanced Generation**: 150+ technical indicator docs in vector store for accurate code generation
- **Live Backtesting**: Test strategies against real market data from Yahoo Finance
- **Performance Metrics**: Sharpe ratio, CAGR, max drawdown, win rate, profit factor
- **Equity Curve Visualization**: See how your strategy performs over time
- **Secure Execution**: Sandboxed code execution with timeout protection

## Tech Stack

**Backend**
- Flask (app factory pattern)
- Claude API (Anthropic) for code generation
- ChromaDB + sentence-transformers for RAG
- pandas-ta for technical indicators
- yfinance for market data

**Frontend**
- React + TypeScript
- Vite
- Recharts for visualization
- Axios for API calls

## Architecture

```
User Input (English)
       |
       v
   React Frontend
       |
       v
   Flask Backend
       |
       +---> RAG Service (ChromaDB)
       |         |
       |         v
       |     Relevant indicator docs
       |         |
       +<--------+
       |
       v
   Claude API (with RAG context)
       |
       v
   Generated Python Code
       |
       v
   Sandbox Execution
       |
       v
   Backtest Results + Metrics
       |
       v
   Equity Curve + Performance Display
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Anthropic API key

### Backend Setup

```bash
cd strategy_builder

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Build the vector store (one-time setup)
python scripts/build_vector_store.py

# Run the backend
python run.py
```

Backend runs at http://127.0.0.1:5000

### Frontend Setup

```bash
cd strategy_builder/frontend

# Install dependencies
npm install

# Run the frontend
npm run dev
```

Frontend runs at http://localhost:5173

## How It Works

1. **User describes a strategy** in plain English (e.g., "Buy when RSI crosses below 30, sell when above 70")

2. **RAG retrieval** finds relevant indicator documentation from the vector store

3. **Claude generates Python code** using the indicator docs as context, ensuring correct pandas-ta syntax

4. **User configures backtest** parameters (ticker, date range)

5. **Sandbox executes the strategy** against real market data with timeout protection

6. **Results display** with performance metrics and equity curve

## Project Structure

```
strategy_builder/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py             # Configuration management
│   ├── corpus/
│   │   └── indicators/       # 160 indicator markdown docs
│   ├── prompts/
│   │   └── system_prompt.txt # Claude system prompt
│   ├── routes/
│   │   └── api.py            # API endpoints
│   ├── services/
│   │   ├── backtest_service.py
│   │   ├── data_service.py
│   │   ├── llm_service.py
│   │   └── rag_service.py
│   └── utils/
│       ├── metrics.py        # Performance calculations
│       └── sandbox.py        # Safe code execution
├── frontend/
│   └── src/
│       ├── components/       # React components
│       ├── services/         # API service
│       └── types/            # TypeScript interfaces
├── scripts/
│   ├── build_corpus.py       # Generate indicator docs
│   └── build_vector_store.py # Build ChromaDB
└── run.py                    # Entry point
```

## Example Strategies

| Strategy | Description |
|----------|-------------|
| RSI Reversal | Buy when RSI crosses below 30, sell when above 70 |
| EMA Crossover | Go long when 10 EMA crosses above 50 EMA |
| Bollinger Bounce | Mean reversion - buy at lower band, sell at upper |
| MACD Crossover | Buy on bullish MACD cross, sell on bearish |

## Key Engineering Decisions

- **RAG over fine-tuning**: Indicator-specific details live in the vector store, not the system prompt. This makes the system maintainable and extensible.

- **Sandboxed execution**: Generated code runs in a restricted environment with limited builtins and timeout protection.

- **Dynamic column handling**: pandas-ta indicators return varying column names. The system uses dynamic column finding patterns to handle this.

## License

MIT
