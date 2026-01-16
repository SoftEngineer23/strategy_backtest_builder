# AO

## Overview
Awesome Oscillator

## pandas-ta Usage
```python
result = df.ta.ao()
```

## Parameters
- fast (default: None)
- slow (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ao()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on AO values

    return signals
```
