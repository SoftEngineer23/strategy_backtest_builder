"""API routes for strategy generation and backtesting."""

from flask import Blueprint, jsonify, request, current_app
from app.services.llm_service import LLMService
from app.services.backtest_service import BacktestService
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok'})

@api_bp.route('/generate', methods=['POST'])
def generate_strategy():
    """
    Generate trading strategy code from description
    Request: {"description": "Buy when RSI < 30"}
    Response: {"success": true, "code": "def strategy(df):...", "error": null}
    """
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'code': None,
            'error': 'Request body must be JSON'
        }), 400

    description = data.get('description', '').strip()

    if not description:
        return jsonify({
            'success': False,
            'code': None,
            'error': 'Description is required'
        }), 400

    # create LLM service and generate
    llm = LLMService(
        api_key=current_app.config['ANTHROPIC_API_KEY'],
        chroma_dir=current_app.config['CHROMA_PERSIST_DIR']
    )
    result = llm.generate_strategy(description)

    return jsonify(result)

@api_bp.route('/backtest', methods=['POST'])
def run_backtest():
  """
  Run backtest on strategy code.

  Request: {"code": "def strategy(df):...", "ticker": "SPY", "start": "2020-01-01", "end": "2024-01-01"}
  Response: {"success": true, "metrics": {...}, "equity_curve": [...], "error": null}
  """
  data = request.get_json()

  if not data:
      return jsonify({
          'success': False,
          'metrics': None,
          'equity_curve': None,
          'error': 'Request body must be JSON'
      }), 400

  # Validate required fields
  required = ['code', 'ticker', 'start', 'end']
  missing = [f for f in required if f not in data]
  if missing:
      return jsonify({
          'success': False,
          'metrics': None,
          'equity_curve': None,
          'error': f'Missing fields: {missing}'
      }), 400

  # Validate date range (max 5 years)
  try:
      start_dt = datetime.strptime(data['start'], '%Y-%m-%d')
      end_dt = datetime.strptime(data['end'], '%Y-%m-%d')

      max_days = 5 * 365
      if (end_dt - start_dt).days > max_days:
          return jsonify({
              'success': False,
              'metrics': None,
              'equity_curve': None,
              'error': 'Date range cannot exceed 5 years'
          }), 400
  except ValueError as e:
      return jsonify({
          'success': False,
          'metrics': None,
          'equity_curve': None,
          'error': f'Invalid date format: {e}'
      }), 400

  # Run backtest
  backtest = BacktestService()
  result = backtest.run_backtest(
      code=data['code'],
      ticker=data['ticker'].upper(),
      start=data['start'],
      end=data['end']
  )

  return jsonify(result)

