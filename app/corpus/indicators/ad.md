# AD

## Overview
Accumulation/Distribution

## pandas-ta Usage
```python
result = df.ta.ad()
```

## Parameters
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ad()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on AD values

    return signals
```
