"""Service for running backtests on generated strategies."""

from app.services.data_service import DataService
from app.utils.sandbox import execute_strategy
from app.utils.metrics import calculate_metrics, calculate_equity_curve


class BacktestService:
  def __init__(self):
      self.data_service = DataService()

  def run_backtest(self, code, ticker, start, end):
      """
      Run a backtest on generated strategy code.

      Args:
          code: Strategy function code
          ticker: Stock symbol
          start: Start date 'YYYY-MM-DD'
          end: End date 'YYYY-MM-DD'

      Returns:
          dict with: success, metrics, equity_curve, error
      """
      # Fetch market data
      data_result = self.data_service.get_data(ticker, start, end)

      if not data_result['success']:
          return {
              'success': False,
              'metrics': None,
              'equity_curve': None,
              'error': f"Data error: {data_result['error']}"
          }

      df = data_result['data']

      # Execute strategy in sandbox
      exec_result = execute_strategy(code, df)

      if not exec_result['success']:
          return {
              'success': False,
              'metrics': None,
              'equity_curve': None,
              'error': f"Execution error: {exec_result['error']}"
          }

      signals = exec_result['signals']

      # Calculate metrics
      try:
          metrics = calculate_metrics(df, signals)
          equity_curve = calculate_equity_curve(df, signals)

          return {
              'success': True,
              'metrics': metrics,
              'equity_curve': equity_curve,
              'error': None,
              'data_points': len(df),
              'date_range': {
                  'start': df.index[0].strftime('%Y-%m-%d'),
                  'end': df.index[-1].strftime('%Y-%m-%d')
              }
          }

      except Exception as e:
          return {
              'success': False,
              'metrics': None,
              'equity_curve': None,
              'error': f"Metrics error: {str(e)}"
          }