# HWC

## Overview
Holt-Winter Channel

## pandas-ta Usage
```python
result = df.ta.hwc()
```

## Parameters
- scalar (default: None)
- channels (default: None)
- na (default: None)
- nb (default: None)
- nc (default: None)
- nd (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.hwc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HWC values

    return signals
```
