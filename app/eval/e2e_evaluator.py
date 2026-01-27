"""
End-to-end evaluator for regression testing.

Runs the full agent pipeline and checks outputs against
golden test cases to detect regressions.
"""

import json
import time
from pathlib import Path
from typing import List

from app.agent.orchestrator import StrategyAgent
from app.agent.types import AgentTrace, DraftStrategy
from app.eval.generation_evaluator import GenerationEvaluator
from app.eval.types import (
    GoldenTestCase,
    E2ETestResult,
    E2EBatchResult,
)


class E2EEvaluator:
    """
    Run end-to-end tests through the full agent.

    Executes golden test cases and checks whether the agent
    produces strategies that meet expected criteria.
    """

    def __init__(
        self,
        agent: StrategyAgent,
        generation_evaluator: GenerationEvaluator
    ):
        """
        Initialize with agent and generation evaluator.

        Args:
            agent: The strategy agent to test.
            generation_evaluator: Evaluator for strategy quality.
        """
        self.agent = agent
        self.generation_evaluator = generation_evaluator

    def evaluate(self, test_case: GoldenTestCase) -> E2ETestResult:
        """
        Run a single end-to-end test.

        Args:
            test_case: Golden test case with expected behavior.

        Returns:
            E2ETestResult with pass/fail and detailed results.
        """
        start_time = time.time()
        failure_reasons = []

        # Run agent
        result = self.agent.run(test_case.query)
        execution_time_ms = (time.time() - start_time) * 1000

        # Check if agent succeeded
        if not result.success or not result.strategy:
            return E2ETestResult(
                test_id=test_case.test_id,
                query=test_case.query,
                passed=False,
                rubric_score=0.0,
                must_include_results={},
                must_not_include_results={},
                strategy_type_match=False,
                indicators_found=[],
                failure_reasons=["Agent did not produce a strategy"] + result.errors,
                execution_time_ms=execution_time_ms,
                trace_summary=self._summarize_trace(result.trace),
                agent_success=False
            )

        strategy = result.strategy

        # Build searchable strategy text
        strategy_text = self._build_strategy_text(strategy).lower()

        # Check must_include terms
        must_include_results = {}
        for term in test_case.must_include:
            found = term.lower() in strategy_text
            must_include_results[term] = found
            if not found:
                failure_reasons.append(f"Missing required term: {term}")

        # Check must_not_include terms
        must_not_include_results = {}
        for term in test_case.must_not_include:
            found = term.lower() in strategy_text
            must_not_include_results[term] = not found  # True = good (not found)
            if found:
                failure_reasons.append(f"Contains forbidden term: {term}")

        # Check strategy type (accept any of the expected types)
        expected_types_lower = [t.lower() for t in test_case.expected_strategy_types]
        strategy_type_match = strategy.strategy_type.lower() in expected_types_lower
        if not strategy_type_match:
            failure_reasons.append(
                f"Strategy type mismatch: expected one of {test_case.expected_strategy_types}, "
                f"got '{strategy.strategy_type}'"
            )

        # Get rubric score via generation evaluator
        draft = DraftStrategy(
            name=strategy.name,
            description=strategy.description,
            strategy_type=strategy.strategy_type,
            components=[],
            entry_rules=strategy.entry_rules,
            exit_rules=strategy.exit_rules,
            risk_management=strategy.risk_management,
            instruments=strategy.instruments,
            timeframe=strategy.timeframe,
            code=strategy.code
        )
        gen_eval = self.generation_evaluator.evaluate(draft, test_case.query)
        rubric_score = gen_eval.rubric_score

        if rubric_score < test_case.min_rubric_score:
            failure_reasons.append(
                f"Rubric score too low: {rubric_score:.1f} < {test_case.min_rubric_score}"
            )

        # Extract indicators found (simple heuristic)
        indicators_found = self._extract_indicators(strategy_text, test_case.expected_indicators)

        # Overall pass/fail
        passed = len(failure_reasons) == 0

        return E2ETestResult(
            test_id=test_case.test_id,
            query=test_case.query,
            passed=passed,
            rubric_score=rubric_score,
            must_include_results=must_include_results,
            must_not_include_results=must_not_include_results,
            strategy_type_match=strategy_type_match,
            indicators_found=indicators_found,
            failure_reasons=failure_reasons,
            execution_time_ms=execution_time_ms,
            trace_summary=self._summarize_trace(result.trace),
            agent_success=True
        )

    def evaluate_batch(self, test_cases: List[GoldenTestCase]) -> E2EBatchResult:
        """
        Evaluate multiple test cases.

        Args:
            test_cases: List of golden test cases.

        Returns:
            E2EBatchResult with aggregated results.
        """
        results = [self.evaluate(tc) for tc in test_cases]
        return E2EBatchResult(results=results)

    def _build_strategy_text(self, strategy) -> str:
        """Build searchable text from strategy."""
        parts = [
            strategy.name,
            strategy.description,
            ' '.join(strategy.entry_rules),
            ' '.join(strategy.exit_rules),
            ' '.join(strategy.risk_management),
            strategy.code or ''
        ]
        return ' '.join(parts)

    def _extract_indicators(self, strategy_text: str, expected: List[str]) -> List[str]:
        """Extract which expected indicators appear in strategy."""
        found = []
        for indicator in expected:
            if indicator.lower() in strategy_text:
                found.append(indicator)
        return found

    def _summarize_trace(self, trace: AgentTrace) -> str:
        """Create brief trace summary."""
        states = ' -> '.join(s.name for s in trace.states_visited)
        return f"{states} | {trace.total_duration_ms:.0f}ms | {trace.total_tokens} tokens"


def load_e2e_tests(data_dir: Path) -> List[GoldenTestCase]:
    """
    Load E2E golden test cases from JSON file.

    Args:
        data_dir: Directory containing e2e_golden_tests.json.

    Returns:
        List of GoldenTestCase objects.
    """
    test_file = data_dir / 'e2e_golden_tests.json'
    if not test_file.exists():
        return []

    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    test_cases = []
    for tc in data.get('test_cases', []):
        # Handle both old format (single type) and new format (list of types)
        if 'expected_strategy_types' in tc:
            expected_types = tc['expected_strategy_types']
        else:
            expected_types = [tc['expected_strategy_type']]

        test_cases.append(GoldenTestCase(
            test_id=tc['test_id'],
            query=tc['query'],
            expected_strategy_types=expected_types,
            must_include=tc['must_include'],
            must_not_include=tc['must_not_include'],
            expected_indicators=tc['expected_indicators'],
            min_rubric_score=tc['min_rubric_score'],
            notes=tc.get('notes', '')
        ))
    return test_cases
