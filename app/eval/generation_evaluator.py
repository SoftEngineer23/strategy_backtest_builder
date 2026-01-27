"""
Generation evaluator for measuring strategy quality.

Evaluates generated strategies using the existing CritiqueTool
plus additional checks for completeness and constraint adherence.
"""

from typing import Dict, List, Optional

from app.agent.tools import CritiqueTool
from app.agent.types import (
    CritiqueStatus,
    DraftStrategy,
    FinalStrategy,
)
from app.eval.types import GenerationEvalResult


class GenerationEvaluator:
    """
    Evaluate generation quality using the critique rubric.

    Wraps the CritiqueTool and adds additional quality checks
    for constraint adherence and component completeness.
    """

    def __init__(self, critique_tool: CritiqueTool):
        """
        Initialize with critique tool.

        Args:
            critique_tool: Tool for strategy critique.
        """
        self.critique_tool = critique_tool

    def evaluate(
        self,
        strategy: DraftStrategy,
        original_request: str,
        expected_constraints: Optional[List[str]] = None
    ) -> GenerationEvalResult:
        """
        Evaluate a generated strategy.

        Args:
            strategy: The strategy to evaluate.
            original_request: Original user query.
            expected_constraints: Optional list of constraints to check.

        Returns:
            GenerationEvalResult with scores and pass/fail status.
        """
        # Run critique tool
        critique_result = self.critique_tool.execute(
            draft_strategy=strategy,
            original_request=original_request
        )

        # Compute rubric score (0-5 scale)
        if critique_result.success and critique_result.result:
            critique = critique_result.result
            rubric_score = self._compute_rubric_score(critique.evaluations)
            critique_passed = critique.overall_pass
            failed_criteria = critique.get_failed_criteria()
        else:
            rubric_score = 0.0
            critique_passed = False
            failed_criteria = ["Critique failed to execute"]

        # Check constraint adherence
        constraint_adherence = self._check_constraints(
            strategy,
            expected_constraints or []
        )

        # Check completeness
        completeness = self._check_completeness(strategy)

        # Overall pass requires critique pass and high completeness
        overall_pass = critique_passed and completeness >= 0.8

        return GenerationEvalResult(
            rubric_score=rubric_score,
            constraint_adherence=constraint_adherence,
            completeness=completeness,
            overall_pass=overall_pass,
            critique_passed=critique_passed,
            failed_criteria=failed_criteria
        )

    def evaluate_final_strategy(
        self,
        strategy: FinalStrategy,
        original_request: str,
        expected_constraints: Optional[List[str]] = None
    ) -> GenerationEvalResult:
        """
        Evaluate a final strategy by converting to draft format.

        Args:
            strategy: The final strategy to evaluate.
            original_request: Original user query.
            expected_constraints: Optional list of constraints to check.

        Returns:
            GenerationEvalResult with scores and pass/fail status.
        """
        # Convert FinalStrategy to DraftStrategy for critique
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

        return self.evaluate(draft, original_request, expected_constraints)

    def _compute_rubric_score(self, evaluations: Dict) -> float:
        """
        Convert critique evaluations to numeric score.

        Args:
            evaluations: Dict of criterion -> CritiqueEvaluation.

        Returns:
            Score on 0-5 scale.
        """
        score_map = {
            CritiqueStatus.PASS: 1.0,
            CritiqueStatus.PARTIAL: 0.5,
            CritiqueStatus.FAIL: 0.0,
            CritiqueStatus.NOT_APPLICABLE: None  # Exclude from average
        }

        scores = []
        for eval_obj in evaluations.values():
            mapped = score_map.get(eval_obj.status)
            if mapped is not None:
                scores.append(mapped)

        if not scores:
            return 0.0

        # Scale to 0-5
        return (sum(scores) / len(scores)) * 5.0

    def _check_completeness(self, strategy: DraftStrategy) -> float:
        """
        Check if all required components are present.

        Args:
            strategy: Strategy to check.

        Returns:
            Completeness fraction (0-1).
        """
        checks = [
            bool(strategy.name),
            bool(strategy.entry_rules),
            bool(strategy.exit_rules),
            bool(strategy.risk_management),
            bool(strategy.code),
        ]
        return sum(checks) / len(checks)

    def _check_constraints(
        self,
        strategy: DraftStrategy,
        expected_constraints: List[str]
    ) -> Dict[str, bool]:
        """
        Check if strategy addresses each constraint.

        Args:
            strategy: Strategy to check.
            expected_constraints: List of constraint descriptions.

        Returns:
            Dict mapping constraint to whether it was addressed.
        """
        if not expected_constraints:
            return {}

        results = {}
        strategy_text = strategy.to_prompt_text().lower()

        for constraint in expected_constraints:
            constraint_lower = constraint.lower()

            # Check based on constraint type
            if 'drawdown' in constraint_lower:
                addressed = any(term in strategy_text for term in
                    ['stop loss', 'stop-loss', 'daily loss', 'max loss', 'drawdown'])
            elif 'win rate' in constraint_lower:
                addressed = 'win rate' in strategy_text or 'probability' in strategy_text
            elif 'position size' in constraint_lower:
                addressed = 'position' in strategy_text or 'size' in strategy_text
            else:
                # Generic check - look for constraint keywords
                addressed = constraint_lower in strategy_text

            results[constraint] = addressed

        return results
