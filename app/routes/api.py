"""API routes for strategy generation and backtesting."""

from pathlib import Path
from flask import Blueprint, jsonify, request, current_app
from app.services.llm_service import LLMService
from app.services.backtest_service import BacktestService
from app.agent.orchestrator import create_agent
from app.agent.tracer import AgentTracer
from datetime import datetime

api_bp = Blueprint('api', __name__)

# In-memory trace store for debugging (in production, use Redis or DB)
_trace_store = {}

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

    # Check if agentic mode is requested
    use_agent = data.get('use_agent', False)
    include_trace = data.get('include_trace', False)

    if use_agent:
        return _generate_with_agent(description, include_trace)

    # Legacy: create LLM service and generate
    llm = LLMService(
        api_key=current_app.config['ANTHROPIC_API_KEY'],
        chroma_dir=current_app.config['CHROMA_PERSIST_DIR']
    )
    result = llm.generate_strategy(description)

    return jsonify(result)


def _generate_with_agent(description: str, include_trace: bool = False):
    """
    Generate strategy using agentic workflow.

    Args:
        description: User's strategy description.
        include_trace: Whether to include execution trace in response.

    Returns:
        JSON response with strategy and optional trace.
    """
    try:
        # Create agent
        agent = create_agent(
            api_key=current_app.config['ANTHROPIC_API_KEY'],
            chroma_dir=Path(current_app.config['CHROMA_PERSIST_DIR']),
            corpus_dir=Path(current_app.config.get('CORPUS_DIR', 'app/corpus')),
            max_iterations=2
        )

        # Run agent
        result = agent.run(description)

        # Store trace for later retrieval
        _trace_store[result.trace.request_id] = result.trace

        # Build response
        response = {
            'success': result.success,
            'code': result.strategy.code if result.strategy else None,
            'error': result.errors[-1] if result.errors else None,
            'warnings': result.warnings,
            'request_id': result.trace.request_id,
        }

        # Include strategy details
        if result.strategy:
            response['strategy'] = {
                'name': result.strategy.name,
                'description': result.strategy.description,
                'strategy_type': result.strategy.strategy_type,
                'entry_rules': result.strategy.entry_rules,
                'exit_rules': result.strategy.exit_rules,
                'risk_management': result.strategy.risk_management,
            }

        # Optionally include trace
        if include_trace:
            tracer = AgentTracer()
            response['trace'] = result.trace.to_dict()
            response['trace_formatted'] = tracer.format_human_readable(result.trace)

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'success': False,
            'code': None,
            'error': f'Agent error: {str(e)}',
            'warnings': [],
        }), 500


@api_bp.route('/trace/<request_id>', methods=['GET'])
def get_trace(request_id: str):
    """
    Retrieve execution trace for a previous agent run.

    Args:
        request_id: The request ID returned from /generate with use_agent=true.

    Returns:
        Trace data and formatted trace string.
    """
    trace = _trace_store.get(request_id)

    if not trace:
        return jsonify({
            'error': f'Trace not found: {request_id}',
            'available_traces': list(_trace_store.keys())[-10:]  # Last 10
        }), 404

    tracer = AgentTracer()
    return jsonify({
        'trace': trace.to_dict(),
        'trace_formatted': tracer.format_human_readable(trace)
    })


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

