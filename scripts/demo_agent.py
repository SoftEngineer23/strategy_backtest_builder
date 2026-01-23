"""
Demo script showing the full agent workflow.

Run with: python scripts/demo_agent.py

This demonstrates the complete agentic workflow:
DECOMPOSE -> RESEARCH -> SYNTHESIZE -> CRITIQUE -> (REFINE ->) COMPLETE

Requires ANTHROPIC_API_KEY environment variable to be set.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / '.env')

from app.agent.orchestrator import create_agent
from app.agent.tracer import AgentTracer


def main():
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Set it in your .env file or export it in your shell")
        return

    # Paths
    chroma_dir = project_root / 'data' / 'chroma'
    corpus_dir = project_root / 'app' / 'corpus'

    print("=" * 65)
    print("STRATEGY BUILDER - AGENTIC WORKFLOW DEMO")
    print("=" * 65)

    # Create agent
    print("\nInitializing agent...")
    agent = create_agent(
        api_key=api_key,
        chroma_dir=chroma_dir,
        corpus_dir=corpus_dir,
        max_iterations=2
    )
    print("Agent ready.\n")

    # Example queries to try
    example_queries = [
        "Build me an RSI reversal strategy that buys when RSI is oversold and sells when overbought",
        "Create a mean reversion strategy using Bollinger Bands with a 5% max drawdown constraint",
        "I want a momentum strategy that uses MACD crossovers for entries",
    ]

    print("Example queries you can try:")
    for i, q in enumerate(example_queries, 1):
        print(f"  {i}. {q}")

    print("\n" + "-" * 65)
    query = input("\nEnter your strategy request (or press Enter for example 1): ").strip()

    if not query:
        query = example_queries[0]
        print(f"\nUsing example: {query}")

    print("\n" + "=" * 65)
    print("RUNNING AGENT")
    print("=" * 65 + "\n")

    # Run the agent
    result = agent.run(query)

    # Print the trace
    tracer = AgentTracer()
    print(tracer.format_human_readable(result.trace))

    # Print the result
    print("\n" + "=" * 65)
    print("RESULT")
    print("=" * 65)

    if result.success:
        print(f"\nStatus: SUCCESS")
        print(f"\nStrategy: {result.strategy.name}")
        print(f"Type: {result.strategy.strategy_type}")
        print(f"Description: {result.strategy.description}")

        print("\nEntry Rules:")
        for rule in result.strategy.entry_rules:
            print(f"  - {rule}")

        print("\nExit Rules:")
        for rule in result.strategy.exit_rules:
            print(f"  - {rule}")

        print("\nRisk Management:")
        for rule in result.strategy.risk_management:
            print(f"  - {rule}")

        if result.strategy.code:
            print("\nGenerated Code:")
            print("-" * 40)
            print(result.strategy.code)
            print("-" * 40)

        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

    else:
        print(f"\nStatus: FAILED")
        print(f"\nErrors:")
        for e in result.errors:
            print(f"  - {e}")

        if result.partial_results:
            print("\nPartial Results:")
            for key, value in result.partial_results.items():
                print(f"  {key}: {value}")

    print("\n" + "=" * 65)


if __name__ == '__main__':
    main()
