# BBANDS

## Overview
Bollinger Bands - volatility bands placed above and below a moving average.

## pandas-ta Usage
```python
bb = df.ta.bbands(length=20, std=2.0)
```

## Return Value
Returns a **DataFrame** with columns for lower, middle, upper bands, bandwidth, and percent.
Column names follow the pattern: BBL_{length}_{std}, BBM_{length}_{std}, BBU_{length}_{std}

To find columns dynamically:
```python
bb = df.ta.bbands(length=20, std=2.0)
bb_lower = bb[[c for c in bb.columns if c.startswith('BBL')][0]]
bb_middle = bb[[c for c in bb.columns if c.startswith('BBM')][0]]
bb_upper = bb[[c for c in bb.columns if c.startswith('BBU')][0]]
```

## Parameters
- length: Period for the moving average (default: 20)
- std: Standard deviation multiplier (default: 2.0) - USE FLOAT like 2.0, not integer
- mamode: Moving average type (default: sma)
- offset: Offset the result (default: 0)

## Example Strategy
```python
def strategy(df):
    # Get Bollinger Bands - returns a DataFrame
    bb = df.ta.bbands(length=20, std=2.0)

    # Extract bands dynamically (handles column name variations)
    bb_lower = bb[[c for c in bb.columns if c.startswith('BBL')][0]].fillna(df['Close'])
    bb_upper = bb[[c for c in bb.columns if c.startswith('BBU')][0]].fillna(df['Close'])

    signals = pd.Series(0, index=df.index)

    # Buy when price touches lower band
    signals[df['Close'] <= bb_lower] = 1

    # Sell when price touches upper band
    signals[df['Close'] >= bb_upper] = -1

    return signals
```
