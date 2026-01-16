# CRSI

## Overview
Connors Relative Strength Index

## pandas-ta Usage
```python
result = df.ta.crsi()
```

## Parameters
- rsi_length (default: None)
- streak_length (default: None)
- rank_length (default: None)
- scalar (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.crsi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CRSI values

    return signals
```
