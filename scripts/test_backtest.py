"""Test that agent-generated code runs through backtest engine."""

import requests
import json

# Code from results3.txt (EMA Cross Expansion Strategy)
# Note: imports removed - sandbox provides pd, np, df.ta
CODE = '''
def strategy(df):
    # Calculate EMAs
    ema9 = df.ta.ema(length=9)
    ema20 = df.ta.ema(length=20)
    atr = df.ta.atr(length=14)

    # Fill NaN values
    ema9 = ema9.fillna(0)
    ema20 = ema20.fillna(0)
    atr = atr.fillna(0)

    # Calculate candle body sizes
    body_size = abs(df['Close'] - df['Open'])
    avg_body_size = body_size.rolling(window=20).mean().fillna(0)

    # Identify EMA crosses
    bullish_cross = (ema9 > ema20) & (ema9.shift(1) <= ema20.shift(1))
    bearish_cross = (ema9 < ema20) & (ema9.shift(1) >= ema20.shift(1))

    # Track bars since cross
    bars_since_bullish_cross = pd.Series(999, index=df.index)
    bars_since_bearish_cross = pd.Series(999, index=df.index)

    for i in range(1, len(df)):
        if bullish_cross.iloc[i]:
            bars_since_bullish_cross.iloc[i] = 0
        else:
            bars_since_bullish_cross.iloc[i] = bars_since_bullish_cross.iloc[i-1] + 1

        if bearish_cross.iloc[i]:
            bars_since_bearish_cross.iloc[i] = 0
        else:
            bars_since_bearish_cross.iloc[i] = bars_since_bearish_cross.iloc[i-1] + 1

    # Identify expansions
    bullish_expansion = (
        (body_size > 1.5 * avg_body_size) &
        (df['Close'] > df['Open']) &
        (body_size > body_size.shift(1))
    )

    bearish_expansion = (
        (body_size > 1.5 * avg_body_size) &
        (df['Close'] < df['Open']) &
        (body_size > body_size.shift(1))
    )

    # Initialize signals and position tracking
    signals = pd.Series(0, index=df.index)
    position = pd.Series(0, index=df.index)
    entry_price = pd.Series(np.nan, index=df.index)
    stop_loss = pd.Series(np.nan, index=df.index)
    take_profit = pd.Series(np.nan, index=df.index)

    for i in range(1, len(df)):
        # Carry forward position
        position.iloc[i] = position.iloc[i-1]
        entry_price.iloc[i] = entry_price.iloc[i-1]
        stop_loss.iloc[i] = stop_loss.iloc[i-1]
        take_profit.iloc[i] = take_profit.iloc[i-1]

        # Entry conditions
        if position.iloc[i] == 0:  # No current position
            # Long entry: bullish expansion after bullish EMA cross
            if (bullish_expansion.iloc[i] and
                ema9.iloc[i] > ema20.iloc[i] and
                bars_since_bullish_cross.iloc[i] <= 10):
                signals.iloc[i] = 1
                position.iloc[i] = 1
                entry_price.iloc[i] = df['Close'].iloc[i]
                stop_loss.iloc[i] = entry_price.iloc[i] - 2 * atr.iloc[i]
                take_profit.iloc[i] = entry_price.iloc[i] + 3 * atr.iloc[i]

            # Short entry: bearish expansion after bearish EMA cross
            elif (bearish_expansion.iloc[i] and
                  ema9.iloc[i] < ema20.iloc[i] and
                  bars_since_bearish_cross.iloc[i] <= 10):
                signals.iloc[i] = -1
                position.iloc[i] = -1
                entry_price.iloc[i] = df['Close'].iloc[i]
                stop_loss.iloc[i] = entry_price.iloc[i] + 2 * atr.iloc[i]
                take_profit.iloc[i] = entry_price.iloc[i] - 3 * atr.iloc[i]

        # Exit conditions
        else:
            # Exit long position
            if position.iloc[i] == 1:
                if (bearish_cross.iloc[i] or  # EMA cross exit
                    df['Low'].iloc[i] <= stop_loss.iloc[i] or  # Stop loss
                    df['High'].iloc[i] >= take_profit.iloc[i]):  # Take profit
                    signals.iloc[i] = -1
                    position.iloc[i] = 0
                    entry_price.iloc[i] = np.nan
                    stop_loss.iloc[i] = np.nan
                    take_profit.iloc[i] = np.nan

            # Exit short position
            elif position.iloc[i] == -1:
                if (bullish_cross.iloc[i] or  # EMA cross exit
                    df['High'].iloc[i] >= stop_loss.iloc[i] or  # Stop loss
                    df['Low'].iloc[i] <= take_profit.iloc[i]):  # Take profit
                    signals.iloc[i] = 1
                    position.iloc[i] = 0
                    entry_price.iloc[i] = np.nan
                    stop_loss.iloc[i] = np.nan
                    take_profit.iloc[i] = np.nan

    return signals
'''

def test_backtest():
    """Run the generated code through the backtest endpoint."""
    url = 'http://127.0.0.1:5000/api/backtest'

    payload = {
        'code': CODE,
        'ticker': 'SPY',
        'start': '2023-01-01',
        'end': '2024-01-01'
    }

    print("Testing backtest with agent-generated code...")
    print(f"Ticker: {payload['ticker']}")
    print(f"Period: {payload['start']} to {payload['end']}")
    print("-" * 50)

    try:
        response = requests.post(url, json=payload)
        result = response.json()

        if result.get('success'):
            print("SUCCESS! Backtest completed.")
            print("\nMetrics:")
            metrics = result.get('metrics', {})
            for key, value in metrics.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")

            equity = result.get('equity_curve', [])
            print(f"\nEquity curve points: {len(equity)}")
            if equity:
                print(f"  Start: ${equity[0].get('equity', 0):,.2f}")
                print(f"  End: ${equity[-1].get('equity', 0):,.2f}")
        else:
            print("FAILED!")
            print(f"Error: {result.get('error')}")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend.")
        print("Make sure the Flask server is running: python run.py")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_backtest()
