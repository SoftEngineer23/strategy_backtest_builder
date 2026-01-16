# ENTROPY

## Overview
Entropy

## pandas-ta Usage
```python
result = df.ta.entropy()
```

## Parameters
- length (default: None)
- base (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.entropy()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ENTROPY values

    return signals
```
