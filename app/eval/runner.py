"""
Evaluation runner that orchestrates all evaluators.

Provides a unified interface to run retrieval, generation,
and end-to-end evaluations with a single command.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from app.eval.types import (
    EvalReport,
    RetrievalTestCase,
    GoldenTestCase,
)
from app.eval.retrieval_evaluator import RetrievalEvaluator, load_retrieval_tests
from app.eval.generation_evaluator import GenerationEvaluator
from app.eval.e2e_evaluator import E2EEvaluator, load_e2e_tests


class EvalRunner:
    """
    Orchestrate all evaluations.

    Loads test data, runs evaluators, and produces reports.
    """

    def __init__(
        self,
        retrieval_evaluator: Optional[RetrievalEvaluator] = None,
        generation_evaluator: Optional[GenerationEvaluator] = None,
        e2e_evaluator: Optional[E2EEvaluator] = None,
        test_data_dir: Optional[Path] = None
    ):
        """
        Initialize with evaluators.

        Args:
            retrieval_evaluator: Evaluator for retrieval tests.
            generation_evaluator: Evaluator for generation quality.
            e2e_evaluator: Evaluator for end-to-end tests.
            test_data_dir: Directory containing test data JSON files.
        """
        self.retrieval_evaluator = retrieval_evaluator
        self.generation_evaluator = generation_evaluator
        self.e2e_evaluator = e2e_evaluator
        self.test_data_dir = test_data_dir or Path(__file__).parent / 'data'

    def run_retrieval(
        self,
        test_cases: Optional[List[RetrievalTestCase]] = None
    ) -> EvalReport:
        """
        Run retrieval evaluation only.

        Args:
            test_cases: Optional list of test cases. If None, loads from file.

        Returns:
            EvalReport with retrieval results.
        """
        if self.retrieval_evaluator is None:
            raise ValueError("Retrieval evaluator not configured")

        if test_cases is None:
            test_cases = load_retrieval_tests(self.test_data_dir)

        if not test_cases:
            raise ValueError("No retrieval test cases found")

        results = self.retrieval_evaluator.evaluate_batch(test_cases)

        return EvalReport(
            timestamp=datetime.now(),
            retrieval=results
        )

    def run_e2e(
        self,
        test_cases: Optional[List[GoldenTestCase]] = None
    ) -> EvalReport:
        """
        Run end-to-end evaluation only.

        Args:
            test_cases: Optional list of test cases. If None, loads from file.

        Returns:
            EvalReport with E2E results.
        """
        if self.e2e_evaluator is None:
            raise ValueError("E2E evaluator not configured")

        if test_cases is None:
            test_cases = load_e2e_tests(self.test_data_dir)

        if not test_cases:
            raise ValueError("No E2E test cases found")

        results = self.e2e_evaluator.evaluate_batch(test_cases)

        return EvalReport(
            timestamp=datetime.now(),
            e2e=results
        )

    def run_all(self) -> EvalReport:
        """
        Run all configured evaluations.

        Returns:
            EvalReport with all results.
        """
        retrieval_results = None
        e2e_results = None

        # Run retrieval if configured
        if self.retrieval_evaluator is not None:
            test_cases = load_retrieval_tests(self.test_data_dir)
            if test_cases:
                retrieval_results = self.retrieval_evaluator.evaluate_batch(test_cases)

        # Run E2E if configured
        if self.e2e_evaluator is not None:
            test_cases = load_e2e_tests(self.test_data_dir)
            if test_cases:
                e2e_results = self.e2e_evaluator.evaluate_batch(test_cases)

        return EvalReport(
            timestamp=datetime.now(),
            retrieval=retrieval_results,
            e2e=e2e_results
        )
