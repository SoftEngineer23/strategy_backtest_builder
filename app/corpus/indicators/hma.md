# HMA

## Overview
Hull Moving Average

## pandas-ta Usage
```python
result = df.ta.hma()
```

## Parameters
- length (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.hma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HMA values

    return signals
```
