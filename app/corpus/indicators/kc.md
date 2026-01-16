# KC

## Overview
Keltner Channels

## pandas-ta Usage
```python
result = df.ta.kc()
```

## Parameters
- length (default: None)
- scalar (default: None)
- tr (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.kc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on KC values

    return signals
```
