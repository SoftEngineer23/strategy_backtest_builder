# RVI

## Overview
Relative Volatility Index

## pandas-ta Usage
```python
result = df.ta.rvi()
```

## Parameters
- length (default: None)
- scalar (default: None)
- refined (default: None)
- thirds (default: None)
- mamode (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.rvi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on RVI values

    return signals
```
