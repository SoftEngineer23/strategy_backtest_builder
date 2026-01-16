# ADX

## Overview
Average Directional Movement

## pandas-ta Usage
```python
result = df.ta.adx()
```

## Parameters
- length (default: None)
- signal_length (default: None)
- adxr_length (default: None)
- scalar (default: None)
- talib (default: None)
- tvmode (default: None)
- mamode (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.adx()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ADX values

    return signals
```
