# SMC

## Overview
Smart Money Concept

## pandas-ta Usage
```python
result = df.ta.smc()
```

## Parameters
- abr_length (default: None)
- close_length (default: None)
- vol_length (default: None)
- percent (default: None)
- vol_ratio (default: None)
- asint (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.smc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SMC values

    return signals
```
