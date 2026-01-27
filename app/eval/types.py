"""
Type definitions for the evaluation harness.

This module defines all data structures used throughout the eval system:
    - Retrieval Types: Test cases and results for retrieval evaluation
    - Generation Types: Results for generation quality evaluation
    - E2E Types: Golden test cases and end-to-end results
    - Report Types: Aggregated evaluation reports
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# =============================================================================
# RETRIEVAL TYPES
# =============================================================================

@dataclass
class RetrievalTestCase:
    """
    A single retrieval evaluation test case.

    Defines a query and the documents that should be retrieved for it.
    Used to measure precision, recall, and MRR of the retrieval system.
    """
    test_id: str
    query: str
    expected_doc_ids: List[str]
    category: str  # retrieval_basic, indicator_lookup, multi_doc, out_of_scope
    notes: Optional[str] = None


@dataclass
class RetrievalEvalResult:
    """
    Result for a single retrieval test case.

    Contains the actual retrieved documents and computed metrics
    comparing them against expected documents.
    """
    test_id: str
    query: str
    expected_doc_ids: List[str]
    retrieved_doc_ids: List[str]
    precision: float
    recall: float
    reciprocal_rank: float
    passed: bool
    notes: str = ""


@dataclass
class RetrievalBatchResult:
    """
    Aggregated results for a batch of retrieval tests.

    Provides summary metrics across all test cases.
    """
    results: List[RetrievalEvalResult]
    avg_precision: float
    avg_recall: float
    avg_mrr: float
    pass_rate: float
    total_cases: int
    passed_cases: int


# =============================================================================
# GENERATION TYPES
# =============================================================================

@dataclass
class GenerationEvalResult:
    """
    Result of evaluating a generated strategy.

    Combines critique results with additional quality checks
    for constraint adherence and completeness.
    """
    rubric_score: float  # 0-5 scale
    constraint_adherence: Dict[str, bool]  # constraint -> was it addressed
    completeness: float  # 0-1 fraction of required components present
    overall_pass: bool
    critique_passed: bool
    failed_criteria: List[str] = field(default_factory=list)
    notes: str = ""


# =============================================================================
# E2E TYPES
# =============================================================================

@dataclass
class GoldenTestCase:
    """
    End-to-end test case with expected behavior.

    Golden tests are hand-crafted cases where we know what
    a good output should look like. Used for regression detection.
    """
    test_id: str
    query: str
    expected_strategy_types: List[str]  # Any of these types is acceptable
    must_include: List[str]  # Terms that MUST appear in output
    must_not_include: List[str]  # Terms that must NOT appear
    expected_indicators: List[str]
    min_rubric_score: float
    notes: str = ""


@dataclass
class E2ETestResult:
    """
    Result of an end-to-end test.

    Captures whether the test passed and detailed information
    about what succeeded or failed.
    """
    test_id: str
    query: str
    passed: bool
    rubric_score: float
    must_include_results: Dict[str, bool]  # term -> was it found
    must_not_include_results: Dict[str, bool]  # term -> was it absent (True = good)
    strategy_type_match: bool
    indicators_found: List[str]
    failure_reasons: List[str]
    execution_time_ms: float
    trace_summary: str
    agent_success: bool = True  # Did the agent complete without errors


@dataclass
class E2EBatchResult:
    """
    Aggregated results for a batch of E2E tests.

    Provides summary statistics across all golden tests.
    """
    results: List[E2ETestResult]
    total_cases: int = 0
    passed_cases: int = 0
    pass_rate: float = 0.0
    avg_rubric_score: float = 0.0
    avg_execution_time_ms: float = 0.0

    def __post_init__(self):
        """Compute aggregates from results."""
        if self.results:
            self.total_cases = len(self.results)
            self.passed_cases = sum(1 for r in self.results if r.passed)
            self.pass_rate = self.passed_cases / self.total_cases if self.total_cases > 0 else 0.0
            self.avg_rubric_score = sum(r.rubric_score for r in self.results) / self.total_cases
            self.avg_execution_time_ms = sum(r.execution_time_ms for r in self.results) / self.total_cases


# =============================================================================
# REPORT TYPES
# =============================================================================

@dataclass
class EvalReport:
    """
    Complete evaluation report.

    Aggregates results from all evaluation layers (retrieval, generation, e2e)
    into a single report that can be printed or saved.
    """
    timestamp: datetime
    retrieval: Optional[RetrievalBatchResult] = None
    e2e: Optional[E2EBatchResult] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize report to dictionary for JSON export."""
        result = {
            'timestamp': self.timestamp.isoformat(),
            'retrieval': None,
            'e2e': None,
        }

        if self.retrieval:
            result['retrieval'] = {
                'avg_precision': self.retrieval.avg_precision,
                'avg_recall': self.retrieval.avg_recall,
                'avg_mrr': self.retrieval.avg_mrr,
                'pass_rate': self.retrieval.pass_rate,
                'total_cases': self.retrieval.total_cases,
                'passed_cases': self.retrieval.passed_cases,
                'failed_tests': [
                    {
                        'test_id': r.test_id,
                        'query': r.query,
                        'expected': r.expected_doc_ids,
                        'retrieved': r.retrieved_doc_ids,
                    }
                    for r in self.retrieval.results if not r.passed
                ],
            }

        if self.e2e:
            result['e2e'] = {
                'pass_rate': self.e2e.pass_rate,
                'total_cases': self.e2e.total_cases,
                'passed_cases': self.e2e.passed_cases,
                'avg_rubric_score': self.e2e.avg_rubric_score,
                'avg_execution_time_ms': self.e2e.avg_execution_time_ms,
                'failed_tests': [
                    {
                        'test_id': r.test_id,
                        'query': r.query,
                        'failure_reasons': r.failure_reasons,
                        'rubric_score': r.rubric_score,
                    }
                    for r in self.e2e.results if not r.passed
                ],
            }

        return result
