# DECAY

## Overview
Decay

## pandas-ta Usage
```python
result = df.ta.decay()
```

## Parameters
- length (default: None)
- mode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.decay()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DECAY values

    return signals
```
