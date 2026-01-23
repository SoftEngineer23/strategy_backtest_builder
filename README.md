# Strategy Builder

An AI-powered trading strategy generator that converts plain English descriptions into executable Python code and backtests them against real market data.

![Demo](demo.gif)

## Features

- **Natural Language to Code**: Describe your trading strategy in plain English, get working Python code
- **Agentic Workflow**: Multi-step state machine with self-critique and refinement loops
- **RAG-Enhanced Generation**: 170+ technical indicator and price action docs in vector store
- **Live Backtesting**: Test strategies against real market data from Yahoo Finance
- **Performance Metrics**: Sharpe ratio, CAGR, max drawdown, win rate, profit factor
- **Execution Tracing**: Full observability into agent decisions and state transitions
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

## Agentic Workflow

The strategy generator uses a state machine architecture that breaks down strategy creation into discrete steps with self-evaluation:

```
User: "Build me an RSI reversal strategy with max 5% drawdown"
                           |
                           v
    +--------------------------------------------------+
    |                   DECOMPOSE                       |
    |  Parse request into structured components:        |
    |  - strategy_type: reversal                        |
    |  - indicators: [RSI]                              |
    |  - constraints: [max_drawdown: 5%]                |
    |  - research_queries: [...]                        |
    +--------------------------------------------------+
                           |
                           v
    +--------------------------------------------------+
    |                   RESEARCH                        |
    |  Retrieve relevant documents from knowledge base: |
    |  - RSI indicator documentation                    |
    |  - Price action reversal patterns                 |
    |  - Risk management techniques                     |
    +--------------------------------------------------+
                           |
                           v
    +--------------------------------------------------+
    |                  SYNTHESIZE                       |
    |  Generate draft strategy with:                    |
    |  - Entry rules                                    |
    |  - Exit rules                                     |
    |  - Risk management                                |
    |  - Executable Python code                         |
    +--------------------------------------------------+
                           |
                           v
    +--------------------------------------------------+
    |                   CRITIQUE                        |
    |  Evaluate against quality criteria:               |
    |  - Are entry rules specific?                      |
    |  - Are exit rules complete?                       |
    |  - Are constraints addressed?                     |
    |  - Is it internally consistent?                   |
    +--------------------------------------------------+
                           |
                  +--------+--------+
                  |                 |
               PASS              FAIL
                  |                 |
                  v                 v
    +-------------+    +------------------------+
    |  COMPLETE   |    |        REFINE          |
    |  Return     |    |  Fix identified issues |
    |  strategy   |    |  (up to 2 iterations)  |
    +-------------+    +------------------------+
                                   |
                                   v
                            Back to CRITIQUE
```

### Why This Architecture?

| Single-Shot Approach | Agentic Approach |
|---------------------|------------------|
| One LLM call | Multiple focused calls |
| No self-checking | Self-critique catches errors |
| Can't fix mistakes | Refinement loop improves output |
| No visibility into reasoning | Full execution trace |

## Example Trace

When you run a strategy through the agent, you get a detailed trace:

```
=================================================================
AGENT TRACE: e270c867
Query: "EMA crossover strategy with RSI filter"
=================================================================

[000.000] STATE: DECOMPOSE
            LLM: Decompose: EMA crossover strategy with RSI filter...
            -> 574 tokens
            Produced: decomposed_request, 5 research queries
            Note: Strategy type: trend_following
            Duration: 4981ms

[004.981] STATE: RESEARCH
            Tool: get_indicator_info(indicator_name='EMA')
            -> OK (18ms)
            Tool: get_indicator_info(indicator_name='RSI')
            -> OK (0ms)
            Tool: retrieve(query='EMA crossover strategy...', category='indicators')
            -> OK (13754ms)
            Produced: research_findings, 6 documents
            Duration: 14139ms

[019.119] STATE: SYNTHESIZE
            Tool: draft_strategy(...)
            -> OK (17063ms)
            LLM: Draft strategy for: EMA crossover strategy...
            -> 2516 tokens
            Produced: draft_strategy, strategy code
            Duration: 17063ms

[036.182] STATE: CRITIQUE
            Tool: critique_strategy(...)
            -> OK (8526ms)
            Produced: critique_result, overall: PASS
            Note: All criteria passed
            Duration: 8526ms

[044.708] STATE: COMPLETE
            Produced: final_strategy
            Duration: 0ms

=================================================================
SUMMARY
=================================================================
Total duration: 44708ms
States visited: DECOMPOSE -> RESEARCH -> SYNTHESIZE -> CRITIQUE -> COMPLETE
Total tokens: 4403
Total tool calls: 9
Result: SUCCESS
=================================================================
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

### Running the Agent Demo

To see the agentic workflow in action:

```bash
cd strategy_builder
.\venv\Scripts\activate

# Interactive demo
python scripts/demo_agent.py
```

Or use the API directly:

```bash
curl -X POST http://127.0.0.1:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "RSI reversal strategy", "use_agent": true, "include_trace": true}'
```

## Project Structure

```
strategy_builder/
|-- app/
|   |-- __init__.py              # Flask app factory
|   |-- config.py                # Configuration management
|   |-- corpus/
|   |   |-- indicators/          # 160 indicator markdown docs
|   |   |-- price_action/        # 12 price action concept docs
|   |-- prompts/
|   |   |-- system_prompt.txt    # Legacy single-shot prompt
|   |-- routes/
|   |   |-- api.py               # API endpoints
|   |-- services/
|   |   |-- backtest_service.py
|   |   |-- data_service.py
|   |   |-- llm_service.py       # Legacy single-shot service
|   |   |-- rag_service.py
|   |-- utils/
|   |   |-- metrics.py           # Performance calculations
|   |   |-- sandbox.py           # Safe code execution
|   |-- agent/                   # Agentic workflow
|       |-- types.py             # Data models and state definitions
|       |-- orchestrator.py      # State machine engine
|       |-- tracer.py            # Execution tracing
|       |-- prompts/             # Externalized prompt templates
|       |   |-- decompose.txt
|       |   |-- synthesize.txt
|       |   |-- critique.txt
|       |   |-- refine.txt
|       |-- tools/               # Agent tools
|       |   |-- retrieve.py      # RAG retrieval
|       |   |-- indicator.py     # Direct doc lookup
|       |   |-- draft.py         # Strategy synthesis
|       |   |-- critique.py      # Quality evaluation
|       |-- states/              # State handlers
|           |-- decompose.py
|           |-- research.py
|           |-- synthesize.py
|           |-- critique.py
|           |-- refine.py
|           |-- complete.py
|-- frontend/
|   |-- src/
|       |-- components/          # React components
|       |-- services/            # API service
|       |-- types/               # TypeScript interfaces
|-- scripts/
|   |-- build_corpus.py          # Generate indicator docs
|   |-- build_vector_store.py    # Build ChromaDB
|   |-- demo_agent.py            # Agent demo script
|-- tests/
|   |-- test_sandbox.py          # Sandbox security tests
|   |-- test_metrics.py          # Metrics calculation tests
|-- run.py                       # Entry point
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/generate` | POST | Generate strategy (set `use_agent: true` for agentic mode) |
| `/api/backtest` | POST | Run backtest on generated code |
| `/api/trace/<id>` | GET | Retrieve execution trace by request ID |

## Example Strategies

| Strategy | Description |
|----------|-------------|
| RSI Reversal | Buy when RSI crosses below 30, sell when above 70 |
| EMA Crossover | Go long when 10 EMA crosses above 50 EMA |
| Bollinger Bounce | Mean reversion - buy at lower band, sell at upper |
| MACD Crossover | Buy on bullish MACD cross, sell on bearish |
| Support/Resistance | Trade reversals at key price levels |

## Key Engineering Decisions

- **Agentic over single-shot**: Breaking the task into steps with self-critique produces more reliable output than a single LLM call.

- **State machine architecture**: Explicit states with defined transitions make the system debuggable and extensible.

- **Externalized prompts**: Prompt templates live in text files, not code. This allows iteration without code changes.

- **RAG over fine-tuning**: Indicator-specific details live in the vector store, not the model. This makes the system maintainable and extensible.

- **Sandboxed execution**: Generated code runs in a restricted environment with limited builtins and timeout protection.

- **Execution tracing**: Every state transition, tool call, and LLM call is recorded for debugging and evaluation.

## License

MIT
