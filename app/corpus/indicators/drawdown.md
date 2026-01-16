# DRAWDOWN

## Overview
Drawdown

## pandas-ta Usage
```python
result = df.ta.drawdown()
```

## Parameters
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.drawdown()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DRAWDOWN values

    return signals
```
