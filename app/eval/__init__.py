"""
Evaluation harness for Strategy Builder.

Provides systematic measurement of retrieval quality, generation quality,
and end-to-end system performance. Enables data-driven iteration on
prompts, retrieval, and system behavior.

Modules:
    - types: Data structures for evaluation
    - retrieval_evaluator: Retrieval quality measurement
    - generation_evaluator: Generation quality measurement
    - e2e_evaluator: End-to-end regression tests
    - runner: Orchestrates all evaluators
    - reporter: Report generation
"""

from app.eval.types import (
    RetrievalTestCase,
    RetrievalEvalResult,
    RetrievalBatchResult,
    GenerationEvalResult,
    GoldenTestCase,
    E2ETestResult,
    E2EBatchResult,
    EvalReport,
)
from app.eval.retrieval_evaluator import RetrievalEvaluator, load_retrieval_tests
from app.eval.generation_evaluator import GenerationEvaluator
from app.eval.e2e_evaluator import E2EEvaluator, load_e2e_tests
from app.eval.runner import EvalRunner
from app.eval.reporter import EvalReporter, load_baseline

__all__ = [
    # Types
    'RetrievalTestCase',
    'RetrievalEvalResult',
    'RetrievalBatchResult',
    'GenerationEvalResult',
    'GoldenTestCase',
    'E2ETestResult',
    'E2EBatchResult',
    'EvalReport',
    # Evaluators
    'RetrievalEvaluator',
    'GenerationEvaluator',
    'E2EEvaluator',
    # Runner and reporter
    'EvalRunner',
    'EvalReporter',
    # Loaders
    'load_retrieval_tests',
    'load_e2e_tests',
    'load_baseline',
]
