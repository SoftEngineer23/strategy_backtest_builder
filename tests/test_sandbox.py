"""Tests for sandbox execution."""

import pytest
import pandas as pd
import numpy as np
from app.utils.sandbox import execute_strategy, SandboxError


@pytest.fixture
def sample_df():
    """Create sample OHLCV data for testing."""
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    data = {
        'Open': [100, 101, 102, 101, 103, 104, 103, 105, 106, 107],
        'High': [102, 103, 104, 103, 105, 106, 105, 107, 108, 109],
        'Low': [99, 100, 101, 100, 102, 103, 102, 104, 105, 106],
        'Close': [101, 102, 101, 103, 104, 103, 105, 106, 107, 108],
        'Volume': [1000] * 10
    }
    return pd.DataFrame(data, index=dates)


class TestExecuteStrategy:
    """Tests for execute_strategy function."""

    def test_valid_strategy_returns_success(self, sample_df):
        """Valid strategy code should execute successfully."""
        code = """
def strategy(df):
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is True
        assert result['error'] is None
        assert isinstance(result['signals'], pd.Series)

    def test_missing_strategy_function_fails(self, sample_df):
        """Code without strategy function should fail."""
        code = """
def other_function(df):
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False
        assert "No 'strategy' function defined" in result['error']

    def test_wrong_return_type_fails(self, sample_df):
        """Strategy returning non-Series should fail."""
        code = """
def strategy(df):
    return [1] * len(df)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False
        assert 'pandas Series' in result['error']

    def test_wrong_length_fails(self, sample_df):
        """Strategy returning wrong length should fail."""
        code = """
def strategy(df):
    return pd.Series([1, 2, 3])
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False
        assert 'length' in result['error'].lower()

    def test_can_use_pandas(self, sample_df):
        """Strategy should have access to pandas."""
        code = """
def strategy(df):
    signals = pd.Series(0, index=df.index)
    signals[df['Close'] > df['Open']] = 1
    return signals
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is True

    def test_can_use_numpy(self, sample_df):
        """Strategy should have access to numpy."""
        code = """
def strategy(df):
    signals = pd.Series(np.where(df['Close'] > 100, 1, 0), index=df.index)
    return signals
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is True

    def test_can_use_pandas_ta(self, sample_df):
        """Strategy should have access to pandas_ta."""
        code = """
def strategy(df):
    rsi = ta.rsi(df['Close'], length=5)
    signals = pd.Series(0, index=df.index)
    signals[rsi < 30] = 1
    return signals
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is True

    def test_can_use_safe_builtins(self, sample_df):
        """Strategy should have access to safe builtins."""
        code = """
def strategy(df):
    n = len(df)
    signals = pd.Series([0] * n, index=df.index)
    for i in range(n):
        if abs(df['Close'].iloc[i] - 100) < 5:
            signals.iloc[i] = 1
    return signals
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is True

    def test_open_is_blocked(self, sample_df):
        """open() should be blocked."""
        code = """
def strategy(df):
    f = open('test.txt', 'w')
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False

    def test_import_is_blocked(self, sample_df):
        """import should be blocked."""
        code = """
import os
def strategy(df):
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False

    def test_eval_is_blocked(self, sample_df):
        """eval() should be blocked."""
        code = """
def strategy(df):
    eval('print("hello")')
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False

    def test_exec_is_blocked(self, sample_df):
        """exec() should be blocked (inside strategy)."""
        code = """
def strategy(df):
    exec('x = 1')
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False

    def test_syntax_error_fails_gracefully(self, sample_df):
        """Syntax errors should be caught."""
        code = """
def strategy(df)
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False
        assert result['error'] is not None

    def test_runtime_error_fails_gracefully(self, sample_df):
        """Runtime errors should be caught."""
        code = """
def strategy(df):
    x = 1 / 0
    return pd.Series([1] * len(df), index=df.index)
"""
        result = execute_strategy(code, sample_df)
        assert result['success'] is False
        assert 'division' in result['error'].lower()

    def test_df_is_not_modified(self, sample_df):
        """Original DataFrame should not be modified."""
        original_close = sample_df['Close'].copy()
        code = """
def strategy(df):
    df['Close'] = 0
    return pd.Series([1] * len(df), index=df.index)
"""
        execute_strategy(code, sample_df)
        pd.testing.assert_series_equal(sample_df['Close'], original_close)


class TestSandboxError:
    """Tests for SandboxError exception."""

    def test_sandbox_error_is_exception(self):
        """SandboxError should be an Exception."""
        assert issubclass(SandboxError, Exception)

    def test_can_raise_sandbox_error(self):
        """Should be able to raise SandboxError."""
        with pytest.raises(SandboxError):
            raise SandboxError("test error")
