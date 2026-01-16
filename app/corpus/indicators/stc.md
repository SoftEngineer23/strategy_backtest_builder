# STC

## Overview
Schaff Trend Cycle

## pandas-ta Usage
```python
result = df.ta.stc()
```

## Parameters
- tc_length (default: None)
- fast (default: None)
- slow (default: None)
- factor (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.stc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on STC values

    return signals
```
