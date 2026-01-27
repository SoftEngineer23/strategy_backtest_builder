"""
Run evaluation harness for Strategy Builder.

Run with: python scripts/run_eval.py [options]

Options:
    --retrieval-only    Run only retrieval evaluation
    --e2e-only          Run only end-to-end evaluation
    --verbose           Show detailed results for each test
    --compare FILE      Compare against baseline JSON file
    --output FILE       Save results to JSON file

Examples:
    python scripts/run_eval.py
    python scripts/run_eval.py --retrieval-only --verbose
    python scripts/run_eval.py --compare results/baseline.json
    python scripts/run_eval.py --output results/eval_2024_01_15.json

Requires ANTHROPIC_API_KEY environment variable to be set.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / '.env')


def main():
    parser = argparse.ArgumentParser(description='Run Strategy Builder evaluation harness')
    parser.add_argument('--retrieval-only', action='store_true', help='Run only retrieval evaluation')
    parser.add_argument('--e2e-only', action='store_true', help='Run only end-to-end evaluation')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed results')
    parser.add_argument('--compare', type=str, help='Compare against baseline JSON file')
    parser.add_argument('--output', '-o', type=str, help='Save results to JSON file')
    args = parser.parse_args()

    # Check for API key (only needed for E2E)
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key and not args.retrieval_only:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Set it in your .env file or export it in your shell")
        print("(Use --retrieval-only to run retrieval eval without API key)")
        return 1

    # Paths
    chroma_dir = project_root / 'data' / 'chroma'
    corpus_dir = project_root / 'app' / 'corpus'
    test_data_dir = project_root / 'app' / 'eval' / 'data'
    results_dir = project_root / 'results'

    # Import here to avoid import errors before path setup
    from app.eval import (
        EvalRunner,
        EvalReporter,
        RetrievalEvaluator,
        GenerationEvaluator,
        E2EEvaluator,
        load_baseline,
    )
    from app.agent.orchestrator import create_agent
    from app.agent.tools import RetrieveTool, CritiqueTool
    from app.services.rag_service import RAGService
    import anthropic

    print("=" * 65)
    print("STRATEGY BUILDER - EVALUATION HARNESS")
    print("=" * 65)

    # Initialize components based on what we're running
    retrieval_evaluator = None
    generation_evaluator = None
    e2e_evaluator = None

    # Retrieval evaluator (no API key needed)
    if not args.e2e_only:
        print("\nInitializing retrieval evaluator...")
        rag_service = RAGService(chroma_dir)
        retrieve_tool = RetrieveTool(rag_service)
        retrieval_evaluator = RetrievalEvaluator(retrieve_tool, top_k=5)

    # E2E evaluator (needs API key)
    if not args.retrieval_only and api_key:
        print("Initializing agent and E2E evaluator...")
        client = anthropic.Anthropic(api_key=api_key)
        critique_tool = CritiqueTool(client)
        generation_evaluator = GenerationEvaluator(critique_tool)

        agent = create_agent(
            api_key=api_key,
            chroma_dir=chroma_dir,
            corpus_dir=corpus_dir,
            max_iterations=2
        )
        e2e_evaluator = E2EEvaluator(agent, generation_evaluator)

    # Create runner
    runner = EvalRunner(
        retrieval_evaluator=retrieval_evaluator,
        generation_evaluator=generation_evaluator,
        e2e_evaluator=e2e_evaluator,
        test_data_dir=test_data_dir
    )

    # Run evaluations
    print("\nRunning evaluations...")
    print("-" * 65)

    if args.retrieval_only:
        report = runner.run_retrieval()
    elif args.e2e_only:
        report = runner.run_e2e()
    else:
        report = runner.run_all()

    # Print report
    reporter = EvalReporter()
    reporter.print_report(report, verbose=args.verbose)

    # Compare against baseline if specified
    if args.compare:
        baseline_path = Path(args.compare)
        if not baseline_path.is_absolute():
            baseline_path = project_root / baseline_path
        baseline = load_baseline(baseline_path)
        if baseline:
            reporter.compare_reports(report, baseline)
        else:
            print(f"\nWARNING: Baseline file not found: {baseline_path}")

    # Save results if specified
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = results_dir / output_path
        reporter.save_report(report, output_path)

    # Return exit code based on results
    if report.retrieval and report.retrieval.pass_rate < 0.5:
        return 1
    if report.e2e and report.e2e.pass_rate < 0.5:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
