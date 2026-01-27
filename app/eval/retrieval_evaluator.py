"""
Retrieval evaluator for measuring RAG quality.

Evaluates whether the retrieval system returns relevant documents
for given queries using precision, recall, and MRR metrics.
"""

import json
from pathlib import Path
from statistics import mean
from typing import List, Optional

from app.agent.tools import RetrieveTool
from app.eval.types import (
    RetrievalTestCase,
    RetrievalEvalResult,
    RetrievalBatchResult,
)


class RetrievalEvaluator:
    """
    Evaluate retrieval quality against ground truth.

    Computes precision, recall, and mean reciprocal rank (MRR)
    for a set of test queries with known relevant documents.
    """

    # Relevance score threshold for out-of-scope detection
    RELEVANCE_THRESHOLD = 0.5

    def __init__(self, retrieve_tool: RetrieveTool, top_k: int = 5):
        """
        Initialize with retrieve tool.

        Args:
            retrieve_tool: Tool for document retrieval.
            top_k: Number of documents to retrieve per query.
        """
        self.retrieve_tool = retrieve_tool
        self.top_k = top_k

    def evaluate(self, test_case: RetrievalTestCase) -> RetrievalEvalResult:
        """
        Run retrieval and compute metrics for a single test case.

        Args:
            test_case: Test case with query and expected documents.

        Returns:
            RetrievalEvalResult with computed metrics.
        """
        # Execute retrieval
        tool_result = self.retrieve_tool.execute(
            query=test_case.query,
            category='all',
            top_k=self.top_k
        )

        # Extract document IDs from results
        if tool_result.success and tool_result.result:
            retrieved_docs = tool_result.result
            retrieved_ids = [doc.doc_id for doc in retrieved_docs]
            avg_relevance = mean([doc.relevance_score for doc in retrieved_docs]) if retrieved_docs else 0.0
        else:
            retrieved_ids = []
            avg_relevance = 0.0

        expected_ids = set(test_case.expected_doc_ids)

        # Handle out-of-scope queries (no expected docs)
        if not expected_ids:
            # For out-of-scope, success means low relevance scores
            passed = avg_relevance < self.RELEVANCE_THRESHOLD or len(retrieved_ids) == 0
            return RetrievalEvalResult(
                test_id=test_case.test_id,
                query=test_case.query,
                expected_doc_ids=test_case.expected_doc_ids,
                retrieved_doc_ids=retrieved_ids,
                precision=1.0 if passed else 0.0,
                recall=1.0,  # N/A for out-of-scope
                reciprocal_rank=0.0,
                passed=passed,
                notes="Out-of-scope query"
            )

        # Compute metrics for normal queries
        retrieved_set = set(retrieved_ids)
        relevant_retrieved = expected_ids & retrieved_set

        precision = len(relevant_retrieved) / len(retrieved_ids) if retrieved_ids else 0.0
        recall = len(relevant_retrieved) / len(expected_ids)

        # Reciprocal rank: 1/position of first relevant doc
        reciprocal_rank = 0.0
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                reciprocal_rank = 1.0 / (i + 1)
                break

        # Pass if we got at least one relevant doc with decent precision
        passed = recall > 0 and precision >= 0.2

        return RetrievalEvalResult(
            test_id=test_case.test_id,
            query=test_case.query,
            expected_doc_ids=test_case.expected_doc_ids,
            retrieved_doc_ids=retrieved_ids,
            precision=precision,
            recall=recall,
            reciprocal_rank=reciprocal_rank,
            passed=passed
        )

    def evaluate_batch(self, test_cases: List[RetrievalTestCase]) -> RetrievalBatchResult:
        """
        Evaluate multiple test cases and aggregate metrics.

        Args:
            test_cases: List of test cases to evaluate.

        Returns:
            RetrievalBatchResult with aggregated metrics.
        """
        results = [self.evaluate(tc) for tc in test_cases]

        # Aggregate metrics
        avg_precision = mean([r.precision for r in results]) if results else 0.0
        avg_recall = mean([r.recall for r in results]) if results else 0.0
        avg_mrr = mean([r.reciprocal_rank for r in results]) if results else 0.0
        passed_count = sum(1 for r in results if r.passed)
        pass_rate = passed_count / len(results) if results else 0.0

        return RetrievalBatchResult(
            results=results,
            avg_precision=avg_precision,
            avg_recall=avg_recall,
            avg_mrr=avg_mrr,
            pass_rate=pass_rate,
            total_cases=len(results),
            passed_cases=passed_count
        )


def load_retrieval_tests(data_dir: Path) -> List[RetrievalTestCase]:
    """
    Load retrieval test cases from JSON file.

    Args:
        data_dir: Directory containing retrieval_tests.json.

    Returns:
        List of RetrievalTestCase objects.
    """
    test_file = data_dir / 'retrieval_tests.json'
    if not test_file.exists():
        return []

    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return [
        RetrievalTestCase(
            test_id=tc['test_id'],
            query=tc['query'],
            expected_doc_ids=tc['expected_doc_ids'],
            category=tc['category'],
            notes=tc.get('notes')
        )
        for tc in data.get('test_cases', [])
    ]
