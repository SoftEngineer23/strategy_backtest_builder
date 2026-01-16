"""Sandbox for safe execution of generated strategy code."""

import pandas as pd
import numpy as np
import pandas_ta
from concurrent.futures import ThreadPoolExecutor, TimeoutError


class SandboxError(Exception):
  """Raised when sandbox execution fails."""
  pass


def execute_strategy(code, df, timeout_seconds=120):
  """
  Execute strategy code in a restricted environment.

  Args:
      code: The strategy function code
      df: OHLCV DataFrame
      timeout_seconds: Max execution time

  Returns:
      dict with: success, signals (Series), error
  """
  # Create restricted globals
  safe_globals = {
      'pd': pd,
      'np': np,
      'ta': pandas_ta,
      '__builtins__': {
          'range': range,
          'len': len,
          'min': min,
          'max': max,
          'abs': abs,
          'sum': sum,
          'round': round,
          'enumerate': enumerate,
          'zip': zip,
          'list': list,
          'dict': dict,
          'tuple': tuple,
          'set': set,
          'str': str,
          'int': int,
          'float': float,
          'bool': bool,
          'True': True,
          'False': False,
          'None': None,
      }
  }

  safe_locals = {}

  def run_code():
      # Execute the function definition
      exec(code, safe_globals, safe_locals)

      if 'strategy' not in safe_locals:
          raise SandboxError("No 'strategy' function defined")

      # Call the strategy with a copy of the data
      df_copy = df.copy()
      signals = safe_locals['strategy'](df_copy)

      return signals

  # Run with timeout
  try:
      with ThreadPoolExecutor(max_workers=1) as executor:
          future = executor.submit(run_code)
          signals = future.result(timeout=timeout_seconds)

      # Validate output
      if not isinstance(signals, pd.Series):
          return {
              'success': False,
              'signals': None,
              'error': 'Strategy must return a pandas Series'
          }

      if len(signals) != len(df):
          return {
              'success': False,
              'signals': None,
              'error': 'Signals length must match DataFrame length'
          }

      return {
          'success': True,
          'signals': signals,
          'error': None
      }

  except TimeoutError:
      return {
          'success': False,
          'signals': None,
          'error': f'Execution timed out after {timeout_seconds} seconds'
      }
  except Exception as e:
      return {
          'success': False,
          'signals': None,
          'error': str(e)
      }