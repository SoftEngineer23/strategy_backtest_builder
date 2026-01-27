# Architecture Deep Dive

## State Machine Design

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

## Why a State Machine?

Three common patterns for agent orchestration: ReAct (reason-act-observe loops), plan-then-execute, and state machines. I chose a state machine because:

- **Predictable workflow** - Strategy generation follows a natural progression (understand -> research -> draft -> validate). ReAct is better suited for open-ended tasks where the path isn't known upfront.
- **Easier to evaluate** - Each state can be tested independently. When something fails, the trace shows exactly which phase broke.
- **Prevents runaway costs** - Explicit state transitions with iteration limits (max 2 refinements) prevent the agent from spiraling. ReAct agents can meander without careful constraints.

## Example Execution Trace

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

## Project Structure

```
app/agent/                    # Agentic workflow
|-- types.py                  # Data models and state definitions
|-- orchestrator.py           # State machine engine
|-- tracer.py                 # Execution tracing
|-- prompts/                  # Externalized prompt templates
|   |-- decompose.txt
|   |-- synthesize.txt
|   |-- critique.txt
|   |-- refine.txt
|-- tools/                    # Agent tools
|   |-- retrieve.py           # RAG retrieval
|   |-- indicator.py          # Direct doc lookup
|   |-- draft.py              # Strategy synthesis
|   |-- critique.py           # Quality evaluation
|-- states/                   # State handlers
    |-- decompose.py
    |-- research.py
    |-- synthesize.py
    |-- critique.py
    |-- refine.py
    |-- complete.py
```

## Key Design Decisions

### Externalized Prompts
Prompt templates live in text files, not code. This allows iteration without code changes and makes A/B testing straightforward.

### RAG over Fine-tuning
Indicator-specific details live in the vector store (170+ docs), not the model. This makes the system maintainable and extensible - add new indicators by adding markdown files.

### Sandboxed Execution
Generated code runs in a restricted environment with:
- Limited builtins (no file I/O, network, imports)
- Timeout protection (30 second max)
- Pre-loaded safe libraries (pandas, numpy, pandas-ta)

### Execution Tracing
Every state transition, tool call, and LLM call is recorded. This enables:
- Debugging failed generations
- Performance profiling
- Evaluation harness integration
