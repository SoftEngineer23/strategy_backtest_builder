# Strategy Builder

An AI-powered trading strategy generator that converts plain English descriptions into executable Python code and backtests them against real market data.

![Demo](demo.gif)

## Features

- **Natural Language to Code**: Describe your trading strategy in plain English, get working Python code
- **Agentic Workflow**: Multi-step state machine with self-critique and refinement loops
- **RAG-Enhanced Generation**: 170+ technical indicator and price action docs in vector store
- **Live Backtesting**: Test strategies against real market data from Yahoo Finance
- **Evaluation Harness**: Automated testing with 40% to 100% improvement through data-driven iteration

## Tech Stack

**Backend**: Flask, Claude API (Anthropic), ChromaDB, pandas-ta, yfinance

**Frontend**: React, TypeScript, Vite, Recharts

## Architecture Highlights

### Why Agentic?

| Single-Shot Approach | Agentic Approach |
|---------------------|------------------|
| One LLM call | Multiple focused calls |
| No self-checking | Self-critique catches errors |
| Can't fix mistakes | Refinement loop improves output |
| No visibility into reasoning | Full execution trace |

### Why a State Machine?

Three common patterns for agent orchestration: ReAct, plan-then-execute, and state machines. I chose a state machine because:

- **Predictable workflow** - Strategy generation follows a natural progression. ReAct is better for open-ended tasks.
- **Easier to evaluate** - Each state can be tested independently. Failures show exactly which phase broke.
- **Prevents runaway costs** - Explicit transitions with iteration limits prevent spiraling.

[See full architecture details](docs/ARCHITECTURE.md)

## Evaluation Harness

Used data-driven iteration to improve E2E pass rate from **40% to 100%**:

| Iteration | Fix                                               | Result |
|-----------|---------------------------------------------------|--------|
| Baseline | -                                                  | 40% (4/10) |
| 1 | Added strategy type definitions to prompt                 | 70% (7/10) |
| 2 | Increased max_tokens for complex strategies               | 80% (8/10) |
| 3 | Expanded acceptance criteria for ambiguous strategy types | 100% (10/10) |

[See full evaluation methodology](docs/EVALUATION.md)

## Quick Start

### Backend

```bash
cd strategy_builder
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

cp .env.example .env
# Add your ANTHROPIC_API_KEY

python scripts/build_vector_store.py  # One-time setup
python run.py
```

### Frontend

```bash
cd strategy_builder/frontend
npm install
npm run dev
```

### Run Evaluation

```bash
python scripts/run_eval.py --verbose
```

## License

MIT
