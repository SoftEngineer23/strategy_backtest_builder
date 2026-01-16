# VIDYA

## Overview
Variable Index Dynamic Average

## pandas-ta Usage
```python
result = df.ta.vidya()
```

## Parameters
- length (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.vidya()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VIDYA values

    return signals
```
