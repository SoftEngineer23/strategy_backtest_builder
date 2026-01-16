"""Service for fetching market data."""

import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime


class DataService:
  def __init__(self, cache_dir='data/cache'):
      self.cache_dir = Path(cache_dir)
      self.cache_dir.mkdir(parents=True, exist_ok=True)

  def get_data(self, ticker, start, end, use_cache=True):
      """
      Fetch OHLCV data for a ticker.

      Args:
          ticker: Stock symbol (e.g., 'SPY', 'AAPL')
          start: Start date 'YYYY-MM-DD'
          end: End date 'YYYY-MM-DD'
          use_cache: Whether to cache results

      Returns:
          dict with: success, data (DataFrame), error
      """
      # Validate dates
      try:
          start_dt = datetime.strptime(start, '%Y-%m-%d')
          end_dt = datetime.strptime(end, '%Y-%m-%d')
      except ValueError as e:
          return {'success': False, 'data': None, 'error': f'Invalid date: {e}'}

      if start_dt >= end_dt:
          return {'success': False, 'data': None, 'error': 'Start must be before end'}

      # Check cache
      cache_key = f"{ticker}_{start}_{end}.csv"
      cache_path = self.cache_dir / cache_key

      if use_cache and cache_path.exists():
          try:
              df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
              return {'success': True, 'data': df, 'error': None}
          except Exception:
              pass

      # Fetch from yfinance
      try:
          df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

          if df.empty:
              return {'success': False, 'data': None, 'error': f'No data for {ticker}'}

          # Flatten multi-level columns if present
          if isinstance(df.columns, pd.MultiIndex):
              df.columns = df.columns.get_level_values(0)

          # Cache it
          if use_cache:
              df.to_csv(cache_path)

          return {'success': True, 'data': df, 'error': None}

      except Exception as e:
          return {'success': False, 'data': None, 'error': str(e)}