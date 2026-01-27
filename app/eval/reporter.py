"""
Report generation for evaluation results.

Provides console output and JSON export for evaluation reports.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.eval.types import EvalReport


class EvalReporter:
    """
    Generate reports from evaluation results.

    Supports console output and JSON export for tracking.
    """

    def print_report(self, report: EvalReport, verbose: bool = False):
        """
        Print human-readable report to console.

        Args:
            report: Evaluation report to print.
            verbose: If True, show individual test results.
        """
        print("\n" + "=" * 65)
        print("EVALUATION REPORT")
        print(f"Timestamp: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        # Retrieval results
        if report.retrieval:
            self._print_retrieval_results(report, verbose)

        # E2E results
        if report.e2e:
            self._print_e2e_results(report, verbose)

        # Summary
        self._print_summary(report)

        print("=" * 65)

    def _print_retrieval_results(self, report: EvalReport, verbose: bool):
        """Print retrieval evaluation results."""
        ret = report.retrieval
        print("\nRETRIEVAL EVALUATION")
        print(f"   Precision:  {ret.avg_precision:.2f}")
        print(f"   Recall:     {ret.avg_recall:.2f}")
        print(f"   MRR:        {ret.avg_mrr:.2f}")
        print(f"   Pass rate:  {ret.pass_rate:.1%} ({ret.passed_cases}/{ret.total_cases})")

        # Show failures
        failures = [r for r in ret.results if not r.passed]
        if failures:
            print("\n   Failed cases:")
            for f in failures[:5]:  # Show first 5
                print(f"   - {f.test_id}: \"{f.query[:40]}...\"")
                print(f"     Expected: {f.expected_doc_ids}")
                print(f"     Got: {f.retrieved_doc_ids[:3]}...")
            if len(failures) > 5:
                print(f"   ... and {len(failures) - 5} more failures")

        if verbose:
            print("\n   All results:")
            for r in ret.results:
                status = "PASS" if r.passed else "FAIL"
                print(f"   [{status}] {r.test_id}: P={r.precision:.2f} R={r.recall:.2f} MRR={r.reciprocal_rank:.2f}")

    def _print_e2e_results(self, report: EvalReport, verbose: bool):
        """Print E2E evaluation results."""
        e2e = report.e2e
        print("\nEND-TO-END TESTS")
        print(f"   Pass rate:  {e2e.pass_rate:.1%} ({e2e.passed_cases}/{e2e.total_cases})")
        print(f"   Avg rubric: {e2e.avg_rubric_score:.1f}/5.0")
        print(f"   Avg time:   {e2e.avg_execution_time_ms / 1000:.1f}s")

        if verbose:
            print("\n   Results:")
            for r in e2e.results:
                status = "PASS" if r.passed else "FAIL"
                print(f"   [{status}] {r.test_id}: {r.rubric_score:.1f}/5.0 ({r.execution_time_ms/1000:.1f}s)")
                if not r.passed:
                    for reason in r.failure_reasons[:2]:
                        print(f"         - {reason}")

        # Show failures
        failures = [r for r in e2e.results if not r.passed]
        if failures and not verbose:
            print("\n   Failures:")
            for f in failures:
                print(f"   - {f.test_id}: {', '.join(f.failure_reasons[:2])}")

    def _print_summary(self, report: EvalReport):
        """Print overall summary."""
        print("\nSUMMARY")

        # Determine overall status
        status = "PASS"
        issues = []

        if report.retrieval:
            if report.retrieval.pass_rate < 0.7:
                status = "NEEDS ATTENTION"
                issues.append(f"Retrieval pass rate low ({report.retrieval.pass_rate:.1%})")
            print(f"   Retrieval:  {report.retrieval.passed_cases}/{report.retrieval.total_cases} passed")

        if report.e2e:
            if report.e2e.pass_rate < 0.7:
                status = "NEEDS ATTENTION"
                issues.append(f"E2E pass rate low ({report.e2e.pass_rate:.1%})")
            if report.e2e.avg_rubric_score < 3.0:
                status = "NEEDS ATTENTION"
                issues.append(f"Avg rubric score low ({report.e2e.avg_rubric_score:.1f})")
            print(f"   E2E:        {report.e2e.passed_cases}/{report.e2e.total_cases} passed")

        print(f"\n   Overall:    {status}")

        if issues:
            print("\n   Issues to address:")
            for issue in issues:
                print(f"   - {issue}")

    def save_report(self, report: EvalReport, output_path: Path):
        """
        Save report to JSON file.

        Args:
            report: Evaluation report to save.
            output_path: Path to output file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2)

        print(f"\nResults saved to: {output_path}")

    def compare_reports(
        self,
        current: EvalReport,
        baseline: EvalReport
    ):
        """
        Compare current results against baseline.

        Args:
            current: Current evaluation report.
            baseline: Baseline report to compare against.
        """
        print("\n" + "=" * 65)
        print("COMPARISON VS BASELINE")
        print("=" * 65)

        # Compare retrieval
        if current.retrieval and baseline.retrieval:
            print("\nRetrieval:")
            self._compare_metric("Precision", baseline.retrieval.avg_precision, current.retrieval.avg_precision)
            self._compare_metric("Recall", baseline.retrieval.avg_recall, current.retrieval.avg_recall)
            self._compare_metric("MRR", baseline.retrieval.avg_mrr, current.retrieval.avg_mrr)
            self._compare_metric("Pass rate", baseline.retrieval.pass_rate, current.retrieval.pass_rate)

        # Compare E2E
        if current.e2e and baseline.e2e:
            print("\nE2E:")
            self._compare_metric("Pass rate", baseline.e2e.pass_rate, current.e2e.pass_rate)
            self._compare_metric("Avg rubric", baseline.e2e.avg_rubric_score, current.e2e.avg_rubric_score)

            # Check for regressions
            if baseline.e2e.results and current.e2e.results:
                baseline_passed = {r.test_id for r in baseline.e2e.results if r.passed}
                current_failed = {r.test_id for r in current.e2e.results if not r.passed}
                regressions = baseline_passed & current_failed

                if regressions:
                    print("\n   Regressions (was PASS, now FAIL):")
                    for test_id in regressions:
                        print(f"   - {test_id}")

        print("\n" + "=" * 65)

    def _compare_metric(self, name: str, baseline: float, current: float):
        """Compare a single metric and show delta."""
        delta = current - baseline
        direction = "+" if delta >= 0 else ""
        indicator = "+" if delta > 0.01 else ("-" if delta < -0.01 else "=")
        print(f"   {name}: {baseline:.2f} -> {current:.2f} ({direction}{delta:.2f}) {indicator}")


def load_baseline(baseline_path: Path) -> Optional[EvalReport]:
    """
    Load baseline report from JSON file.

    Args:
        baseline_path: Path to baseline JSON file.

    Returns:
        EvalReport or None if file doesn't exist.
    """
    if not baseline_path.exists():
        return None

    with open(baseline_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Reconstruct report from dict (simplified - doesn't restore full results)
    from app.eval.types import RetrievalBatchResult, E2EBatchResult

    retrieval = None
    if data.get('retrieval'):
        r = data['retrieval']
        retrieval = RetrievalBatchResult(
            results=[],
            avg_precision=r['avg_precision'],
            avg_recall=r['avg_recall'],
            avg_mrr=r['avg_mrr'],
            pass_rate=r['pass_rate'],
            total_cases=r['total_cases'],
            passed_cases=r['passed_cases']
        )

    e2e = None
    if data.get('e2e'):
        e = data['e2e']
        e2e = E2EBatchResult(
            results=[],
            total_cases=e['total_cases'],
            passed_cases=e['passed_cases'],
            pass_rate=e['pass_rate'],
            avg_rubric_score=e['avg_rubric_score'],
            avg_execution_time_ms=e['avg_execution_time_ms']
        )

    return EvalReport(
        timestamp=datetime.fromisoformat(data['timestamp']),
        retrieval=retrieval,
        e2e=e2e
    )
