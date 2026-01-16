# DONCHIAN

## Overview
Donchian Channels

## pandas-ta Usage
```python
result = df.ta.donchian()
```

## Parameters
- lower_length (default: None)
- upper_length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.donchian()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DONCHIAN values

    return signals
```
