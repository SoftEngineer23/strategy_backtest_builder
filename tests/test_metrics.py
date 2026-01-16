"""Tests for performance metrics calculations."""

import pytest
import pandas as pd
import numpy as np
from app.utils.metrics import calculate_metrics, calculate_equity_curve, _empty_metrics


@pytest.fixture
def sample_df():
    """Create sample OHLCV data for testing."""
    dates = pd.date_range('2023-01-01', periods=20, freq='D')
    # Create an uptrend: prices go from 100 to 119
    closes = list(range(100, 120))
    data = {
        'Open': [c - 1 for c in closes],
        'High': [c + 1 for c in closes],
        'Low': [c - 2 for c in closes],
        'Close': closes,
        'Volume': [1000] * 20
    }
    return pd.DataFrame(data, index=dates)


@pytest.fixture
def all_long_signals(sample_df):
    """Signals that are always long, with matching index."""
    return pd.Series([1] * len(sample_df), index=sample_df.index)


@pytest.fixture
def all_flat_signals(sample_df):
    """Signals that are always flat (no position), with matching index."""
    return pd.Series([0] * len(sample_df), index=sample_df.index)


class TestCalculateMetrics:
    """Tests for calculate_metrics function."""

    def test_returns_dict_with_expected_keys(self, sample_df, all_long_signals):
        """Verify all expected metric keys are returned."""
        result = calculate_metrics(sample_df, all_long_signals)

        expected_keys = [
            'total_return', 'cagr', 'sharpe_ratio', 'max_drawdown',
            'win_rate', 'num_trades', 'avg_trade_return', 'profit_factor'
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_all_long_positive_returns(self, sample_df, all_long_signals):
        """All long in uptrend should have positive returns."""
        result = calculate_metrics(sample_df, all_long_signals)
        assert result['total_return'] > 0

    def test_all_flat_zero_returns(self, sample_df, all_flat_signals):
        """Flat signals should have zero returns."""
        result = calculate_metrics(sample_df, all_flat_signals)
        assert result['total_return'] == 0
        assert result['win_rate'] == 0

    def test_sharpe_ratio_calculation(self, sample_df, all_long_signals):
        """Sharpe ratio should be a number."""
        result = calculate_metrics(sample_df, all_long_signals)
        assert isinstance(result['sharpe_ratio'], (int, float))

    def test_max_drawdown_is_negative_or_zero(self, sample_df, all_long_signals):
        """Max drawdown should be <= 0."""
        result = calculate_metrics(sample_df, all_long_signals)
        assert result['max_drawdown'] <= 0

    def test_win_rate_between_0_and_100(self, sample_df, all_long_signals):
        """Win rate should be between 0 and 100."""
        result = calculate_metrics(sample_df, all_long_signals)
        assert 0 <= result['win_rate'] <= 100

    def test_empty_dataframe_returns_empty_metrics(self):
        """Empty data should return empty metrics."""
        empty_df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        signals = pd.Series([], dtype=float)
        result = calculate_metrics(empty_df, signals)
        assert result == _empty_metrics()

    def test_alternating_signals(self, sample_df):
        """Test with alternating long/short signals."""
        alternating = [1, -1] * (len(sample_df) // 2)
        signals = pd.Series(alternating, index=sample_df.index)
        result = calculate_metrics(sample_df, signals)
        assert result['num_trades'] > 0


class TestCalculateEquityCurve:
    """Tests for calculate_equity_curve function."""

    def test_returns_list(self, sample_df, all_long_signals):
        """Equity curve should return a list."""
        result = calculate_equity_curve(sample_df, all_long_signals)
        assert isinstance(result, list)

    def test_each_point_has_date_and_value(self, sample_df, all_long_signals):
        """Each point should have date and value keys."""
        result = calculate_equity_curve(sample_df, all_long_signals)
        for point in result:
            assert 'date' in point
            assert 'value' in point

    def test_dates_are_strings(self, sample_df, all_long_signals):
        """Dates should be formatted as strings."""
        result = calculate_equity_curve(sample_df, all_long_signals)
        if result:
            assert isinstance(result[0]['date'], str)

    def test_values_are_numbers(self, sample_df, all_long_signals):
        """Values should be numeric."""
        result = calculate_equity_curve(sample_df, all_long_signals)
        if result:
            assert isinstance(result[0]['value'], (int, float))

    def test_starts_near_one(self, sample_df, all_long_signals):
        """Equity curve should start near 1.0."""
        result = calculate_equity_curve(sample_df, all_long_signals)
        if result:
            assert 0.9 <= result[0]['value'] <= 1.1


class TestEmptyMetrics:
    """Tests for _empty_metrics function."""

    def test_returns_dict(self):
        """Should return a dictionary."""
        result = _empty_metrics()
        assert isinstance(result, dict)

    def test_all_values_are_zero(self):
        """All values should be zero."""
        result = _empty_metrics()
        for key, value in result.items():
            assert value == 0, f"{key} is not zero"
